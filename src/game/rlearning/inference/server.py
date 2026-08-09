import queue
import signal
import time
import traceback
from collections import OrderedDict

import numpy as np
import torch

from game.rlearning.inference.protocol import InferenceResponse, PolicyUpdate
from game.rlearning.utils.data import batch_to_cuda
from game.rlearning.utils.file import read_yaml
from game.rlearning.utils.model import get_class_by_name


class BatchedInferenceServer:
    """Owns policy models and batches rollout requests on one CUDA device."""

    def __init__(self, communication, config: dict):
        self.communication = communication
        self.max_batch_size = config.get("max_batch_size", 32)
        self.max_wait_seconds = config.get("max_wait_ms", 5) / 1000
        self.max_cached_policies = config.get("max_cached_policies", 8)
        self.policies = OrderedDict()
        self.running = True

    def _load_policy(self, config_path: str, restore_step, force: bool = False):
        key = (config_path, str(restore_step))
        current = self.policies.get(key)
        if current and not force:
            self.policies.move_to_end(key)
            return current["trainer"]
        if current:
            del self.policies[key]

        config = read_yaml(config_path)
        trainer_class = get_class_by_name(config["trainer"])
        trainer = trainer_class(config, restore_step, name=f"inference:{key[1]}")
        trainer.pbar = None
        self.policies[key] = {
            "trainer": trainer,
            "config_path": config_path,
            "restore_step": restore_step,
        }
        while len(self.policies) > self.max_cached_policies:
            _, evicted = self.policies.popitem(last=False)
            del evicted
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return trainer

    def _apply_controls(self):
        while True:
            try:
                command = self.communication.control_queue.get_nowait()
            except queue.Empty:
                return
            if command == "stop":
                self.running = False
                return
            if isinstance(command, PolicyUpdate):
                self._load_policy(command.config_path, command.restore_step, force=True)

    @torch.no_grad()
    def _infer_group(self, requests):
        first = requests[0]
        trainer = self._load_policy(first.config_path, first.restore_step)
        samples = [trainer.dataset.get_sample_preprocess(request.state) for request in requests]
        batch = trainer.dataset.collate_state(samples)
        batch = batch_to_cuda(batch, trainer.rank)
        for model in trainer.models.values():
            model.eval()
        batch = trainer.predict(batch, trainer.models, False, trainer.step, trainer.epoch)
        scores = batch["actions"]
        masks = torch.as_tensor(
            np.concatenate([request.state["mask"] for request in requests], axis=0),
            dtype=torch.bool,
            device=scores.device,
        )
        scores = scores.masked_fill(~masks, 0)
        actions = torch.distributions.Categorical(scores).sample().detach().cpu().tolist()
        return actions, first.restore_step

    def _respond_error(self, request, error: str):
        self.communication.response_queues[request.worker_id].put(
            InferenceResponse(request.request_id, 0, request.restore_step, error)
        )

    def run(self):
        while self.running:
            self._apply_controls()
            if not self.running:
                break
            try:
                first = self.communication.request_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            requests = [first]
            deadline = time.monotonic() + self.max_wait_seconds
            while len(requests) < self.max_batch_size:
                self._apply_controls()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                try:
                    requests.append(self.communication.request_queue.get(timeout=remaining))
                except queue.Empty:
                    break

            groups = {}
            for request in requests:
                # The actual model identity is its config and checkpoint.  A
                # policy_id is only a rollout-side label, so workers using the
                # same model can still share one GPU batch.
                key = (request.config_path, request.restore_step)
                groups.setdefault(key, []).append(request)
            for group in groups.values():
                try:
                    actions, version = self._infer_group(group)
                    for request, action in zip(group, actions):
                        self.communication.response_queues[request.worker_id].put(
                            InferenceResponse(request.request_id, action, version)
                        )
                except Exception:
                    error = traceback.format_exc()
                    for request in group:
                        self._respond_error(request, error)


def inference_server_process(communication, config: dict):
    # The parent process owns Ctrl+C and sends an explicit stop command.
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    BatchedInferenceServer(communication, config).run()
