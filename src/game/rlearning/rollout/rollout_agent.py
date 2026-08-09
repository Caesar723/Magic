from game.rlearning.inference.client import InferenceClient
from game.rlearning.inference.protocol import RestoreStep
from game.rlearning.utils.common import CHECKPOINT_ROOT_PATH
from game.rlearning.utils.file import read_yaml
from initinal_file import ORGPATH


class RolloutBuffer:
    def __init__(self):
        self.datas = []

    def store_data(self, data: dict):
        self.datas.append({
            "state": data["state"], "action": data["action"],
            "reward": data["reward"], "next_state": data["next_state"],
            "done": data["done"], "global_reward": data["global_reward"],
        })


class RolloutAgent:
    """Compatibility layer for Agent_Train without a local torch model."""

    def __init__(self, config_path: str, communication, worker_id: int, policy_id: str,
                 restore_step: RestoreStep = 0):
        self.config_path = config_path
        self.config = read_yaml(config_path)
        self.name = policy_id
        self.pbar = None
        # GameRecorder keeps its existing per-policy output location.  The
        # rollout process does not own a trainer, but it still needs these two
        # metadata fields used by Base_Agent_Room.
        self.logdir = f"{ORGPATH}/../{CHECKPOINT_ROOT_PATH}/{self.config['log_dir']}"
        self.step = self._numeric_step(restore_step)
        self.dataset = RolloutBuffer()
        self.client = InferenceClient(
            communication, worker_id, policy_id, config_path, restore_step
        )

    def choose_action(self, batch, extra_keys=None, isTrain=False):
        if len(batch) != 1:
            raise ValueError("RolloutAgent expects one environment state per request")
        return self.client.choose_action(batch[0])

    def store(self, data: dict):
        self.dataset.store_data(data)

    def restore_checkpoint(self, restore_step):
        self.client.configure(restore_step=restore_step)
        self.step = self._numeric_step(restore_step)

    @staticmethod
    def _numeric_step(restore_step):
        try:
            return max(int(restore_step), 0)
        except (TypeError, ValueError):
            return 0
