from torch.multiprocessing import Queue
from initinal_file import ORGPATH


class Info_Communication:
    def __init__(self, env_config, manager):
        self.env_config = env_config

        self.task_queue = Queue()
        self.data_queue = Queue()
        self.load_queue = Queue()
        self.ready_queue = Queue()

        self.current_task = None

    def set_current_task(self, task):
        self.current_task = task

    def get_model_info(self, worker_id):
        task = self.current_task

        return {
            "success_update": task is not None,
            "model_update_steps": task["agent_step"] if task else 0,
            "model_path": task["agent_step"] if task else 0,

            "success_opponent_update": task is not None,

            "config_opponent_path": (
                task["opponent_config"]
                if task else
                f"{ORGPATH}/{self.env_config['opponent_config'][0]}"
            ),

            "model_opponent_path": (
                task["opponent_step"] if task else 0
            ),
        }

    def get_task(self):
        return self.task_queue.get()

    def store_game_data(self, data):
        self.data_queue.put(data)

    def get_game_data(self, timeout=None):
        return self.data_queue.get(timeout=timeout)