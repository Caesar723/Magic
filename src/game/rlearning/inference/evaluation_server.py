import queue
import signal
import traceback
import torch

from game.rlearning.inference.server import BatchedInferenceServer


class EvaluationInferenceServer(BatchedInferenceServer):
    deterministic_actions = True

    def __init__(self, communication, config, load_queue):
        super().__init__(communication, config)
        self.load_queue = load_queue

    def _apply_controls(self):
        while True:
            try:
                command = self.communication.control_queue.get_nowait()
            except queue.Empty:
                return

            if command == "stop":
                self.running = False
                return

            try:
                for role, config_path, step in command["policies"]:
                    step = int(step)

                    if role == "main":
                        key = ("main", config_path)
                    elif role == "opponent":
                        key = ("opponent", config_path, step)
                    else:
                        raise ValueError(f"Unknown policy role: {role}")

                    self._load_policy(config_path, step, policy_key=key)

                result = {"id": command["id"], "error": None}
            except Exception:
                result = {"id": command["id"], "error": traceback.format_exc()}

            self.load_queue.put(result)

    @torch.no_grad()
    def _infer_group(self, requests):
        first = requests[0]
        step = int(first.restore_step)

        if first.policy_id == "main":
            key = ("main", first.config_path)
        else:
            key = ("opponent", first.config_path, step)

        trainer = self._load_policy(first.config_path, step, policy_key=key)
        trainer.deterministic_actions = True
        results = trainer.inference([request.state for request in requests], isTrain=False)
        return results, step


def evaluation_server_process(communication, config, load_queue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    server = EvaluationInferenceServer(communication, config, load_queue)
    server.run()