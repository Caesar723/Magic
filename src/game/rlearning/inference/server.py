import queue
import signal
import time
import traceback
from copy import deepcopy
import torch

from game.rlearning.inference.protocol import InferenceResponse, PolicyUpdate
from game.rlearning.utils.file import read_yaml
from game.rlearning.utils.model import get_class_by_name


class BatchedInferenceServer:
    """Owns policy models and batches rollout requests on one CUDA device."""

    def __init__(self, communication, config: dict):
        self.communication = communication
        self.max_batch_size = config.get("max_batch_size", 32)
        self.max_wait_seconds = config.get("max_wait_ms", 5) / 1000
        self.policies = {}
        self.running = True

    def _load_policy(self, config_path, restore_step, force=False):
        try:
            step = int(restore_step)
        except (TypeError, ValueError):
            step = restore_step

        version = str(step)
        current = self.policies.get(config_path)

        if current is None:
            config = read_yaml(config_path)
            trainer_class = get_class_by_name(config["trainer"])

            trainer = trainer_class(
                config, 0, name="inference:shared"
            )
            trainer.pbar = None

            initial_weights = {
                name: deepcopy({
                    key: value.detach().cpu()
                    if torch.is_tensor(value) else value
                    for key, value in model.state_dict().items()
                })
                for name, model in trainer._models.items()
            }

            current = {
                "trainer": trainer,
                "restore_step": None,
                "initial_weights": initial_weights,
            }
            self.policies[config_path] = current

        trainer = current["trainer"]

        if not force and current["restore_step"] == version:
            return trainer

        current["restore_step"] = None

        if step == 0:
            for name, state in current["initial_weights"].items():
                model = trainer._models[name]
                model.load_state_dict(state, strict=False)

                evaluation_model = trainer.models_test[name]
                if evaluation_model is not model:
                    evaluation_model.load_state_dict(
                        state, strict=False
                    )

            trainer.step = 0
            trainer.epoch = 0
        else:
            trainer.restore_checkpoint(step)

        current["restore_step"] = version
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
    def _infer_group(self,requests):
        first=requests[0]
        trainer=self._load_policy(first.config_path,first.restore_step)
        states=[request.state for request in requests]
        results=trainer.inference(states,isTrain=False)
        return results,first.restore_step

    def _respond_error(self,request,error):
        response=InferenceResponse(
            request_id=request.request_id,
            result={},
            policy_version=request.restore_step,
            error=error
        )
        self.communication.response_queues[request.worker_id].put(response)

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
                    results,version=self._infer_group(group)

                    if len(results)!=len(group):
                        raise RuntimeError(f"inference returned {len(results)} results for {len(group)} requests")

                    for request,result in zip(group,results):
                        response=InferenceResponse(
                            request_id=request.request_id,
                            result=result,
                            policy_version=version
                        )
                        self.communication.response_queues[request.worker_id].put(response)
                except Exception:
                    error=traceback.format_exc()
                    for request in group:
                        self._respond_error(request,error)


def inference_server_process(communication, config: dict):
    # The parent process owns Ctrl+C and sends an explicit stop command.
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    BatchedInferenceServer(communication, config).run()
