import multiprocessing as mp
import os
import signal
import sys
import time
import traceback
from copy import deepcopy

from initinal_file import ORGPATH
from game.rlearning.parallel_env.training_parallel_env import Parallel_Env
from game.rlearning.utils.file import read_yaml


if __name__ == "__main__":
    from pathlib import Path

    src_root = next(parent for parent in Path(__file__).resolve().parents if parent.name == "src")
    if str(src_root) not in sys.path:
        sys.path.append(str(src_root))


def run_one_parallel_env(env_config: dict, restore_step):
    """Run one trainable agent in its own process group."""
    try:
        os.setsid()
    except (AttributeError, OSError):
        # Pair exercise runs on Linux, but keeping this fallback preserves
        # importability on platforms without POSIX process groups.
        pass

    env = None
    checkpoint_attempted = False

    def save_checkpoint_once():
        """Persist this child agent without obscuring a preceding failure."""
        nonlocal checkpoint_attempted
        if checkpoint_attempted:
            return

        checkpoint_attempted = True
        agent = getattr(env, "agent1", None)
        if agent is None or agent.rank != 0:
            return

        try:
            agent.save_checkpoint()
        except Exception:
            traceback.print_exc()

    def handle_stop(signum, frame):
        """Turn the first shutdown signal into a graceful local stop."""
        del signum, frame
        if not checkpoint_attempted:
            raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, handle_stop)

    try:
        env = Parallel_Env(env_config, restore_step=restore_step)
        env.start_worker()
        env.run()
    except KeyboardInterrupt:
        # shutdown() uses SIGTERM; the trainer belongs to this child process,
        # so it must write its checkpoint here rather than in the launcher.
        save_checkpoint_once()
    except Exception:
        save_checkpoint_once()
        raise
    finally:
        if env is not None:
            env.shutdown()


class Parallel_Env_Pair_Exercise:
    GRACEFUL_SHUTDOWN_SECONDS = 20
    FORCE_SHUTDOWN_SECONDS = 5
    PROCESS_POLL_SECONDS = 0.1

    def __init__(self, config_path: str, restore_step=None):
        self.config = read_yaml(config_path)
        self.restore_step = restore_step
        self.env_configs = self.build_env_configs(self.config)
        self.processes = {}

    @staticmethod
    def build_env_configs(config: dict):
        """Create one environment configuration for each trainable agent."""
        agent_configs = config["train_config"]
        shared_config = {
            "env": config["env"],
            "info_communication": config["info_communication"],
            "room": config["room"],
            "inference": config["inference"],
            "rollout_torch_threads": config["rollout_torch_threads"],
            "num_worker": config["num_worker"],
        }

        env_configs = []
        for index, agent_config in enumerate(agent_configs):
            opponents = agent_configs[:index] + agent_configs[index + 1 :]
            env_configs.append(
                {
                    **deepcopy(shared_config),
                    "agent_config": agent_config,
                    "opponent_config": deepcopy(opponents),
                }
            )
        return env_configs

    def start_worker(self):
        for index, env_config in enumerate(self.env_configs):
            process = mp.Process(
                target=run_one_parallel_env,
                args=(env_config, self.restore_step),
                name=f"pair-exercise-{index:02d}",
            )
            process.start()
            self.processes[index] = process

    def run(self):
        while self.processes:
            self.collect_finished_processes()
            if self.processes:
                time.sleep(self.PROCESS_POLL_SECONDS)

    def collect_finished_processes(self):
        """Join completed children and surface their failures to the launcher."""
        finished_indices = [
            index
            for index, process in self.processes.items()
            if not process.is_alive()
        ]

        for index in finished_indices:
            process = self.processes.pop(index)
            process.join()
            if process.exitcode != 0:
                raise RuntimeError(
                    f"pair exercise {index} exited with exit code {process.exitcode}"
                )

    def shutdown(self):
        """Save every live child agent, then stop all of its descendants."""
        processes = list(self.processes.values())

        # SIGTERM becomes KeyboardInterrupt in run_one_parallel_env, which
        # saves each child process's agent1 checkpoint before local cleanup.
        for process in processes:
            if process.is_alive():
                process.terminate()

        self.wait_for_processes(processes, self.GRACEFUL_SHUTDOWN_SECONDS)

        # A blocked child can leave rollout workers, inference, or Manager
        # descendants alive.  Signal the complete process group next.
        for process in processes:
            self.signal_process_group(process.pid, signal.SIGTERM)

        self.wait_for_processes(processes, self.FORCE_SHUTDOWN_SECONDS)

        # CUDA workers that ignore SIGTERM must not survive the launcher.
        for process in processes:
            self.signal_process_group(process.pid, signal.SIGKILL)
            if process.is_alive():
                process.kill()

        for process in processes:
            process.join(timeout=1)

        self.processes.clear()

    @staticmethod
    def wait_for_processes(processes, timeout_seconds):
        """Wait until all processes exit or the shutdown deadline is reached."""
        deadline = time.monotonic() + timeout_seconds
        while any(process.is_alive() for process in processes):
            if time.monotonic() >= deadline:
                return
            time.sleep(Parallel_Env_Pair_Exercise.PROCESS_POLL_SECONDS)

    @staticmethod
    def signal_process_group(pid, signal_number):
        """Signal only the process group rooted at a pair child process."""
        if pid is None or os.name != "posix":
            return

        try:
            os.killpg(pid, signal_number)
        except (PermissionError, ProcessLookupError):
            pass
