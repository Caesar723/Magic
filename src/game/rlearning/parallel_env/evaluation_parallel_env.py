import hashlib
import json
import random
import time
import uuid
from copy import deepcopy
from pathlib import Path
from queue import Empty
from torch.multiprocessing import Process

from initinal_file import ORGPATH

from game.rlearning.utils.baseParallelEnv import BaseParallelEnv
from game.rlearning.utils.common import CHECKPOINT_ROOT_PATH
from game.rlearning.utils.file import read_yaml
from game.rlearning.utils.model import get_class_by_name

from game.rlearning.inference.evaluation_server import evaluation_server_process


class Parallel_Env(BaseParallelEnv):

    def __init__(
        self,
        config_path,
        agent_config=None,
        restore_step=None,
    ):
        if isinstance(config_path, dict):
            config = deepcopy(config_path)
        else:
            config = read_yaml(self.source_path(config_path))

        if agent_config is not None:
            config["agent_config"] = agent_config

        if "agent_config" not in config:
            raise ValueError("Agent config is required")

        main_config = read_yaml(
            self.source_path(config["agent_config"])
        )

        config["evaluation"].setdefault(
            "output_dir",
            str(
                Path(CHECKPOINT_ROOT_PATH)
                / main_config["log_dir"]
                / "evaluation"
            ),
        )

        super().__init__(config, restore_step=restore_step)

    def initinal_config(self, config):
        self.info_communication = get_class_by_name(config["info_communication"])(config, self.manager)

        self.room_class = get_class_by_name(config["room"])

        self.config_path = self.source_path(config["agent_config"])
        self.config = read_yaml(self.config_path)

        self.evaluation_config = config["evaluation"]

        self.score_function = get_class_by_name(config["evaluation_function"])

        self.ready = False
        self.active = None

        self.opponent_configs = {}
        self.opponent_steps = {}

        overrides = self.evaluation_config.get("opponent_steps", {})

        for relative_path in config["opponent_config"]:
            path = self.source_path(relative_path)
            opponent = read_yaml(path)

            self.opponent_configs[path] = opponent

            requested = overrides.get(relative_path, opponent["restore_step"])

            self.opponent_steps[path] = self.checkpoint_step(path, requested)

        self.cases = self.build_cases()

        if not self.cases:
            raise ValueError("Evaluation tasks cannot be empty")

        identity = {
            "evaluation": self.evaluation_config,
            "agent_config": self.config,
            "opponent_configs": self.opponent_configs,
            "opponent_steps": self.opponent_steps,
            "cases": self.cases,
            "room": config["room"],
        }

        self.benchmark_id = hashlib.sha256(
            json.dumps(
                identity,
                sort_keys=True,
            ).encode()
        ).hexdigest()[:16]

    @staticmethod
    def source_path(path):
        return str((Path(ORGPATH) / path).resolve())

    @staticmethod
    def decks(config):
        values = config.get("decks")
        return list(values) if values else [config["cards"]]

    def checkpoint_step(self, config_path, step):
        config = read_yaml(config_path)

        folder = (
            Path(CHECKPOINT_ROOT_PATH)
            / config["log_dir"]
            / "ckpt"
        )

        step = int(step)

        if step == -1:
            g = (folder / "g_last").resolve(strict=True)
            i = (folder / "i_last").resolve(strict=True)

            step = int(g.name.removeprefix("g_"))

            if i.name != f"i_{step}":
                raise RuntimeError(
                    "g_last and i_last are not from the same version, please try again later"
                )

        if step <= 0:
            raise ValueError(
                "Please use a positive checkpoint number that has been saved for formal evaluation"
            )

        for prefix in ("g", "i"):
            path = folder / f"{prefix}_{step}"

            if not path.is_file():
                raise FileNotFoundError(path)

        return step

    def build_cases(self):
        rng = random.Random(
            self.evaluation_config["seed"]
        )

        agent_decks = self.decks(self.config)

        indices = self.evaluation_config.get(
            "agent_deck_indices",
            list(range(len(agent_decks))),
        )

        pairs = int(
            self.evaluation_config["pairs_per_matchup"]
        )

        if pairs <= 0 or len(set(indices)) != len(indices):
            raise ValueError("pairs_per_matchup must be a positive number, and the deck indices cannot be repeated")

        cases = []

        for opponent_path, config in self.opponent_configs.items():
            agent_index = rng.choice(indices)
            if not 0 <= agent_index < len(agent_decks):
                raise ValueError(f"Invalid agent deck index: {agent_index}")

            for opponent_index, opponent_deck in enumerate(
                self.decks(config)
            ):
                matchup = (
                    f"{opponent_path}"
                    f"|{agent_index}"
                    f"|{opponent_index}"
                )

                for opening in range(pairs):
                    seeds = [
                        rng.randrange(2**32)
                        for _ in range(3)
                    ]

                    # The same sequence, swap the first and second player.
                    for first_player in ("Agent1", "Agent2"):
                        cases.append({
                            "match_id": len(cases),
                            "matchup": matchup,
                            "opening": opening,

                            "opponent_config": opponent_path,
                            "opponent_step": (
                                self.opponent_steps[opponent_path]
                            ),

                            "agent_deck": agent_decks[agent_index],
                            "opponent_deck": opponent_deck,

                            "first_player": first_player,

                            "agent_shuffle_seed": seeds[0],
                            "opponent_shuffle_seed": seeds[1],
                            "game_seed": seeds[2],
                        })

        return cases

    def check_processes(self):
        processes = [
            self.inference_process,
            *self.worker_process,
        ]

        for process in processes:
            if not process.is_alive():
                raise RuntimeError(
                    "Evaluation process exited: "
                    f"pid={process.pid}, "
                    f"exitcode={process.exitcode}"
                )

    def load_policies(self, policies):
        command_id = uuid.uuid4().hex

        self.inference_communication.control_queue.put({
            "id": command_id,
            "policies": policies,
        })

        deadline = time.monotonic() + (
            self.evaluation_config.get("load_timeout", 300)
        )

        while time.monotonic() < deadline:
            self.check_processes()

            try:
                result = self.info_communication.load_queue.get(
                    timeout=0.2
                )
            except Empty:
                continue

            if result["id"] != command_id:
                raise RuntimeError("Received unexpected model load notification")

            if result["error"]:
                raise RuntimeError(result["error"])

            return

        raise TimeoutError("Evaluation model load timeout")

    def start_worker(self):
        self.inference_process = Process(
            target=evaluation_server_process,
            args=(
                self.inference_communication,
                self.env_config["inference"],
                self.info_communication.load_queue,
            ),
        )

        try:
            super().start_worker()


            self.load_policies([
                (self.config_path, 0), # The model to be evaluated is created first.
                *self.opponent_steps.items(), # The opponents are loaded with fixed checkpoints.
            ])

            workers = set()

            deadline = time.monotonic()+self.evaluation_config.get("load_timeout", 300)
            

            while len(workers) < self.num_worker:
                self.check_processes()

                if time.monotonic() >= deadline:
                    raise TimeoutError("Evaluation room initialization timeout")

                try:
                    worker_id = self.info_communication.ready_queue.get(timeout=0.2)
                    workers.add(worker_id)

                except Empty:
                    continue

            self.ready = True

        except Exception:
            self.shutdown()
            raise

    def start_evaluation(self, restore_step):
        if not self.ready:
            raise RuntimeError("Please call start_worker() first")

        if self.active is not None:
            raise RuntimeError("The previous evaluation has not been completed")

        step = self.checkpoint_step(self.config_path, restore_step)

        try:
            self.load_policies([(self.config_path, step)])

        except Exception:
            self.shutdown()
            raise

        evaluation_id = uuid.uuid4().hex

        self.active = {
            "id": evaluation_id,
            "step": step,
            "results": {},
            "started": time.monotonic(),
        }

        for case in self.cases:
            self.info_communication.task_queue.put({
                **case,
                "evaluation_id": evaluation_id,
                "agent_step": step,
            })

        return evaluation_id

    def poll_evaluation(self):
        if self.active is None:
            return None

        try:
            self.check_processes()

            timeout = self.evaluation_config.get("evaluation_timeout", 3600)

            if time.monotonic() - self.active["started"] > timeout:
                raise TimeoutError("This evaluation timed out, stopping the evaluation service to clear incomplete requests")

            while True:
                try:
                    row = self.info_communication.data_queue.get_nowait()
                except Empty:
                    break

                if row["evaluation_id"] != self.active["id"]:
                    raise RuntimeError("Received results from another evaluation")

                key = row["match_id"]

                if not 0 <= key < len(self.cases):
                    raise RuntimeError("Received unknown match ID")

                if key in self.active["results"]:
                    raise RuntimeError("Received duplicate match results")

                self.active["results"][key] = row

            if len(self.active["results"]) < len(self.cases):
                return None

            rows = [
                self.active["results"][index]
                for index in range(len(self.cases))
            ]

            report = self.score_function(rows)

            report.update({
                "evaluation_id": self.active["id"],
                "step": self.active["step"],
                "benchmark_id": self.benchmark_id,
                "opponent_steps": self.opponent_steps,
                "games": len(rows),
            })

            output = Path(self.evaluation_config["output_dir"])
            output.mkdir(parents=True, exist_ok=True)

            path = output / f"{self.active['id']}.json"

            with path.open("w", encoding="utf-8") as file:
                json.dump({
                    "report": report,
                    "results": rows,
                    "config": self.env_config,
                }, file, ensure_ascii=False, indent=2)

            self.active = None
            return report

        except Exception:
            self.shutdown()
            raise

    def evaluate(self, restore_step):
        self.start_evaluation(restore_step)

        while True:
            report = self.poll_evaluation()

            if report is not None:
                return report

            time.sleep(0.05)

    def run(self):
        if self.restore_step_override is None:
            raise ValueError("Command line evaluation requires using -r to specify a checkpoint")

        return self.evaluate(self.restore_step_override)

    def shutdown(self):
        self.ready = False

        for _ in getattr(self, "worker_process", []):
            self.info_communication.task_queue.put(None)

        for process in getattr(self, "worker_process", []):
            process.join(timeout=1)

        super().shutdown()