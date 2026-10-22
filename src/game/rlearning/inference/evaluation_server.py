import queue
import signal
import traceback

from game.rlearning.inference.server import BatchedInferenceServer


class EvaluationInferenceServer(BatchedInferenceServer):
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
                for config_path, step in command["policies"]:
                    self._load_policy(config_path, step)

                result = {
                    "id": command["id"],
                    "error": None,
                }

            except Exception:
                result = {
                    "id": command["id"],
                    "error": traceback.format_exc(),
                }

            self.load_queue.put(result)


def evaluation_server_process(communication, config, load_queue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    server = EvaluationInferenceServer(
        communication,
        config,
        load_queue,
    )
    server.run()