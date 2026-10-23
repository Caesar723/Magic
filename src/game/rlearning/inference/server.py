import queue
import signal
import time
import traceback
from copy import deepcopy
import torch
import random

from initinal_file import ORGPATH
from game.rlearning.utils.common import CHECKPOINT_ROOT_PATH
from game.rlearning.utils.agentSchedule import AgentSchedule
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

    def _load_policy(self, config_path, restore_step, force=False, policy_key=None):
        try:
            step = int(restore_step)
        except (TypeError, ValueError):
            step = restore_step

        version = str(step)
        key = config_path if policy_key is None else policy_key
        current = self.policies.get(key)

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
            self.policies[key] = current

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
                key = (
                    request.config_path,
                    request.restore_step,
                    request.policy_id == "main",
                )
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


class TrainingInferenceServer(BatchedInferenceServer):
    def __init__(self, communication, config):
        super().__init__(communication, config)

        settings = config["opponent_registration"]
        limits = settings.get("per_config", {})

        self.pool = {
            f"{ORGPATH}/{path}": {
                "step": None,
                "used": 0,
                "active": set(),
                "limit": int(limits.get(
                    path, settings.get("games_per_checkpoint", 20)
                )),
            }
            for path in config["opponent_config"]
        }

        if not self.pool or any(item["limit"] <= 0 for item in self.pool.values()):
            raise ValueError("Opponent configs and positive limits are required")

        self.rooms = {}
        self.waiting = {}
    def change_checkpoint(self, path):
        item = self.pool[path]

        if item["active"]:
            raise RuntimeError("Opponent still has active games")

        config = read_yaml(path)
        logdir = f"{CHECKPOINT_ROOT_PATH}/{config['log_dir']}"
        step = int(AgentSchedule.get_restore_step(logdir))

        if step < 0:
            raise ValueError("Opponent needs a fixed checkpoint number")

        self._load_policy(path, step, policy_key=("opponent", path))
        item.update(step=step, used=0)

    def release_room(self, worker_id):
        self.waiting.pop(worker_id, None)
        path = self.rooms.pop(worker_id, None)

        if path is not None:
            item = self.pool[path]
            item["active"].remove(worker_id)

            if item["used"] >= item["limit"] and not item["active"]:
                self.change_checkpoint(path)

    def assign_rooms(self):
        for worker_id in list(self.waiting):
            available = [
                path for path, item in self.pool.items()
                if item["used"] < item["limit"]
            ]

            if not available:
                return

            path = random.choice(available)
            item = self.pool[path]

            if item["step"] is None:
                self.change_checkpoint(path)

            item["used"] += 1
            item["active"].add(worker_id)
            self.rooms[worker_id] = path
            del self.waiting[worker_id]

            self.communication.response_queues[worker_id].put({
                "config_path": path,
                "restore_step": item["step"],
            })

    def _apply_controls(self):
        while True:
            try:
                command = self.communication.control_queue.get_nowait()
            except queue.Empty:
                break

            if command == "stop":
                self.running = False
                return

            if isinstance(command, PolicyUpdate):
                self._load_policy(command.config_path, command.restore_step)

            elif isinstance(command, tuple) and command[0] in ("opponent", "release"):
                action, worker_id = command
                self.release_room(worker_id)
                if action == "opponent":
                    self.waiting[worker_id] = None
            else:
                raise TypeError(f"Unknown control command: {command}")

        self.assign_rooms()

    @torch.no_grad()
    def _infer_group(self, requests):
        first = requests[0]

        if first.policy_id == "main":
            if first.config_path not in self.policies:
                self._load_policy(first.config_path, first.restore_step)
            trainer = self.policies[first.config_path]["trainer"]

            results = trainer.inference(
                [request.state for request in requests],isTrain=False
            )
            return results, trainer.step

        for request in requests:
            if self.rooms.get(request.worker_id) != request.config_path:
                raise RuntimeError("Opponent has no matching registration")

            step = self.pool[request.config_path]["step"]
            if str(step) != str(request.restore_step):
                raise RuntimeError("Opponent checkpoint does not match")

        trainer = self.policies[("opponent", first.config_path)]["trainer"]
        results = trainer.inference(
            [request.state for request in requests], isTrain=False
        )
        return results, self.pool[first.config_path]["step"]

def inference_server_process(communication, config):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    server_class = (
        TrainingInferenceServer
        if config.get("opponent_registration") is not None
        else BatchedInferenceServer
    )

    server_class(communication, config).run()
