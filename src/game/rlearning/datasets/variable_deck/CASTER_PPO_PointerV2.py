import os
from tqdm import tqdm

import game.rlearning.utils.log as log
from game.rlearning.datasets.variable_deck.CASTER_PPO_Pointer import PPOAgentDataset as PreviousDataset
from game.rlearning.datasets.variable_deck.CASTER_PPO_Pointer import scalar_value


class PPOAgentDataset(PreviousDataset):
    def __init__(self, config):
        settings = config.get("rollout_batch", {})
        self.target_trajectories = int(settings.get("size", 512))
        self.max_policy_lag = int(settings.get("max_policy_lag", 4))

        if self.target_trajectories <= 0:
            raise ValueError("rollout_batch.size must be positive")
        if self.max_policy_lag < 0:
            raise ValueError("rollout_batch.max_policy_lag cannot be negative")

        self.trajectory_count = 0
        self.rejected_trajectories = 0
        self.pending_trajectory = []

        self.policy_generations = {}
        self.current_version = None
        self.current_generation = -1

        # The parent constructor still requires this key.
        # build_segments() below keeps each episode complete.
        parent_config = config.copy()
        parent_config.setdefault("train_seq_len", 32)
        super().__init__(parent_config)

    def _new_pbar(self):
        if os.environ.get("RL_ROLLOUT_WORKER") == "1":
            return None
        return tqdm(total=self.target_trajectories, desc="Storing Trajectories", unit="trajectory")

    def register_policy_version(self, version):
        # Count model publications instead of optimizer steps.
        version = int(version)

        if version < 0:
            raise ValueError("Policy version must be an actual checkpoint step")
        if version == self.current_version:
            return
        if self.current_version is not None and version < self.current_version:
            raise ValueError("Published checkpoint steps must increase")

        self.current_generation += 1
        self.current_version = version
        self.policy_generations[version] = self.current_generation

        # Keep only the versions that are still allowed.
        minimum_generation = self.current_generation - self.max_policy_lag
        allowed_versions = {}

        for step, generation in self.policy_generations.items():
            if generation >= minimum_generation:
                allowed_versions[step] = generation

        self.policy_generations = allowed_versions

    def trajectory_is_fresh(self, trajectory):
        if self.current_version is None:
            raise RuntimeError("Register the initial policy version before collecting data")

        # An episode may contain actions from several model versions.
        for item in trajectory:
            record = item["state"]["decision_record"]

            if "policy_version" not in record:
                raise KeyError("decision_record is missing policy_version")

            version = int(record["policy_version"])
            if version not in self.policy_generations:
                return False

        return True

    def store_data(self, data):
        # Support callers that submit one transition at a time.
        self.pending_trajectory.append(data)

        if bool(scalar_value(data["done"])):
            self.store_round_data(self.pending_trajectory)
            self.pending_trajectory = []

    def store_round_data(self, datas):
        if not datas:
            return

        # Split the message at episode boundaries.
        trajectories = []
        start = 0

        for index, item in enumerate(datas):
            if bool(scalar_value(item["done"])):
                trajectories.append(datas[start:index + 1])
                start = index + 1

        if start != len(datas):
            raise ValueError("Every submitted trajectory must end with done=True")

        # Validate the whole message before changing the training buffer.
        accepted = []
        for trajectory in trajectories:
            accepted.append(self.trajectory_is_fresh(trajectory))

        for trajectory, is_fresh in zip(trajectories, accepted):
            if not is_fresh:
                self.rejected_trajectories += 1
                continue

            self.datas.extend(dict(item) for item in trajectory)
            self.trajectory_count += 1

        if self.pbar is not None:
            self.pbar.n = self.trajectory_count
            self.pbar.set_postfix(transitions=len(self.datas), refresh=False)
            self.pbar.refresh()

            if self.is_full():
                self.pbar.close()
                self.pbar = None

    def is_full(self):
        return self.trajectory_count >= self.target_trajectories

    def build_segments(self):
        # One complete episode becomes one training sample.
        segments = []
        start = 0

        for index, item in enumerate(self.datas):
            if bool(scalar_value(item["done"])):
                segments.append((start, index + 1))
                start = index + 1

        if start != len(self.datas):
            raise ValueError("The training buffer contains an incomplete trajectory")
        if len(segments) != self.trajectory_count:
            raise RuntimeError("Trajectory count does not match the training buffer")

        self.segments = segments

    def clear_data(self):
        if self.pbar is not None:
            self.pbar.close()

        self.trajectory_count = 0
        self.pending_trajectory = []

        # Preserve publication history and cumulative rejection statistics.
        super().clear_data()

    def log_data(self, trainer, batch_extra):
        results = []

        for item in self.datas:
            if bool(scalar_value(item["done"])):
                result = scalar_value(item["next_state"]["terminal_result"])
                results.append(float(result))

        games = len(results)
        transitions = len(self.datas)

        if games == 0 or transitions == 0:
            return

        wins = sum(result == 1.0 for result in results)
        losses = sum(result == -1.0 for result in results)
        draws = sum(result == 0.0 for result in results)

        success_rate = wins / games
        reward_sum = float(batch_extra["reward"].sum().item())
        potential_sum = sum(batch_extra["global_reward"])

        metrics = {
            "success_rate": success_rate,
            "loss_rate": losses / games,
            "draw_rate": draws / games,
            "reward_train": reward_sum / transitions,
            "global_reward": potential_sum / transitions,
            "rollout/episode_return_mean": reward_sum / games,
            "rollout/trajectories": games,
            "rollout/transitions": transitions,
            "rollout/trajectory_length_mean": transitions / games,
            "rollout/rejected_trajectories_total": self.rejected_trajectories,
        }

        for name, value in metrics.items():
            log.sw_scalar(name, value, trainer.step)

        # Preserve the existing checkpoint selection behavior.
        filename = None

        if success_rate > 0.8:
            filename = "great_model.txt"
        elif success_rate > 0.6:
            filename = "good_model.txt"

        if filename is not None:
            path = os.path.join(self.logdir, filename)
            with open(path, "a", encoding="utf-8") as file:
                file.write(f"{trainer.step}\n")