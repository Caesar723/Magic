import sys
if __name__=="__main__":

    from pathlib import Path
    src_root = next(parent for parent in Path(__file__).resolve().parents if parent.name == "src")
    if str(src_root) not in sys.path:
        sys.path.append(str(src_root))
    

import random
import asyncio
import os
import signal
from os import PathLike
from copy import deepcopy

from game.rlearning.utils.model import get_class_by_name
from game.rlearning.utils.file import read_yaml
from game.rlearning.inference.communication import InferenceCommunication
from initinal_file import ORGPATH
from multiprocessing import Queue,Manager,Process
from queue import Full, Empty
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.rlearning.communicate.training_parallel_room import Info_Communication
    from game.rlearning.utils.baseAgent import BaseTrainer

class BaseParallelEnv:
    
    
    def __init__(self, config_path: "str | PathLike | dict", restore_step=None):
        if isinstance(config_path, dict):
            self.env_config = deepcopy(config_path)
        else:
            self.env_config = read_yaml(str(config_path))

        self.restore_step_override = restore_step
        self.num_worker=self.env_config["num_worker"]
        self._init_runtime()
        self.manager=Manager()
        try:
            self.initinal_config(self.env_config)
        except Exception:
            self.manager.shutdown()
            raise

        self.inference_communication = None
        self.inference_process = None
        if "inference" in self.env_config:
            from game.rlearning.inference.server import inference_server_process
            inference_config = {
                **self.env_config["inference"],
                "device_index": self.inference_device,
                "opponent_config": self.env_config["opponent_config"],
            }
            self.inference_communication=InferenceCommunication(
                self.num_worker,
                self.env_config["inference"].get("input_packing")
            )
            self.inference_process = Process(
                target=inference_server_process,
                args=(self.inference_communication, inference_config),
            )
        
        

    def initinal_config(self,config:dict):
        
        self.info_communication:"Info_Communication"=get_class_by_name(self.env_config["info_communication"])(self.env_config,self.manager)

        self.room_class=get_class_by_name(config["room"])
        agent_config=config["agent_config"]
        self.config_path=f"{ORGPATH}/{agent_config}"
        self.config=read_yaml(self.config_path)

        restore_step = self.config["restore_step"]
        if self.restore_step_override is not None:
            restore_step = self.restore_step_override
            self.config["restore_step"] = restore_step

        self.config.setdefault("runtime", {})["device_index"] = self.training_device
        trainer1=get_class_by_name(self.config["trainer"])

        self.agent1:"BaseTrainer"=trainer1(self.config, restore_step, name="main")
        # Workers receive their initial model version through this channel.
        # Keep them aligned with `-r`, including the special latest value -1.
        self.info_communication.update_model(restore_step, restore_step)

    def _init_runtime(self):
        runtime = self.env_config.get("runtime", {})
        hosts = runtime.get("learner_hosts", {"training": {"device": 0, "policies": ["main"]}})
        services = runtime.get("inference_services", {"rollout": {}})

        if not isinstance(hosts, dict) or len(hosts) != 1:
            raise ValueError("This stage supports exactly one learner host")

        if not isinstance(services, dict) or len(services) != 1:
            raise ValueError("This stage supports exactly one inference service")

        host = next(iter(hosts.values()))
        service = next(iter(services.values()))

        if not isinstance(host, dict) or not isinstance(service, dict):
            raise ValueError("Runtime host and service settings must be mappings")

        if host.get("policies", ["main"]) != ["main"]:
            raise ValueError("This stage supports only the main learner")

        evaluation = runtime.get("evaluation", {})
        if not isinstance(evaluation, dict):
            raise ValueError("runtime.evaluation must be a mapping")

        self.training_device = host.get("device", 0)
        self.inference_device = service.get("device", self.training_device)
        self.evaluation_device = evaluation.get("device", self.training_device)

        for name in ("training_device", "inference_device", "evaluation_device"):
            index = getattr(self, name)
            if type(index) is not int or index < 0:
                raise ValueError(f"{name} must be a non-negative integer")

    def start_worker(self):
        if self.inference_process is not None:
            self.inference_process.start()
        self.worker_process=[Process(target=worker_process, args=(
            self.env_config, self.info_communication, self.inference_communication, i, self.room_class
        )) for i in range(self.num_worker)]
        for i in range(self.num_worker):
            self.worker_process[i].start()

        

    def run(self):
        pass

    def stop_inference_server(self):
        if self.inference_process is None:
            return
        if self.inference_process.is_alive():
            self.inference_communication.control_queue.put("stop")
            self.inference_process.join(timeout=10)
            if self.inference_process.is_alive():
                self.inference_process.terminate()
                self.inference_process.join()

    def shutdown(self):
        """Stop all child processes when training completes or receives Ctrl+C."""
        for process in getattr(self, "worker_process", []):
            if process.is_alive():
                process.terminate()
        for process in getattr(self, "worker_process", []):
            process.join(timeout=5)
        self.stop_inference_server()
        if self.manager is not None:
            self.manager.shutdown()
            self.manager = None

    def check_workers(self):
        if self.inference_process is not None and not self.inference_process.is_alive():
            process = self.inference_process
            raise RuntimeError(f"Inference server exited: {process.exitcode} (pid={process.pid})")

        for worker_id, process in enumerate(self.worker_process):
            if not process.is_alive():
                registration = self.env_config.get("inference", {}).get("opponent_registration")
                if registration is not None and self.inference_communication is not None:
                    self.inference_communication.control_queue.put(("release", worker_id))
                raise RuntimeError(f"Worker {worker_id} exited: {process.exitcode} (pid={process.pid})")

async def run_parallel_room(
    env_config,
    info_communication,
    inference_communication,
    worker_id:int,
    room_class:type):
    if inference_communication is None:
        room = room_class(env_config, info_communication, worker_id)
    else:
        room = room_class(env_config, info_communication, worker_id, inference_communication)

    await room.game_start()
    await room.action_process_system()

def worker_process(
    env_config,
    info_communication,
    inference_communication,
    worker_id:int,
    room_class:type):
    os.environ["RL_ROLLOUT_WORKER"] = "1"
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    if inference_communication is None:
        import torch
        torch.set_num_threads(env_config.get("rollout_torch_threads",1))
    try:
        asyncio.run(run_parallel_room(
            env_config,
            info_communication,
            inference_communication,
            worker_id,
            room_class,
        ))
    finally:
        registration = env_config.get("inference", {}).get("opponent_registration")
        if registration is not None and inference_communication is not None:
            inference_communication.control_queue.put(("release", worker_id))
