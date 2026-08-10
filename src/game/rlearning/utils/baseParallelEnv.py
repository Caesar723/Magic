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

from game.rlearning.utils.model import get_class_by_name
from game.rlearning.utils.file import read_yaml
from game.rlearning.inference.communication import InferenceCommunication
from game.rlearning.inference.server import inference_server_process
from initinal_file import ORGPATH
from torch.multiprocessing import Queue,Manager,Process
from queue import Full, Empty
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.rlearning.communicate.training_parallel_room import Info_Communication
    from game.rlearning.utils.baseAgent import BaseTrainer

class BaseParallelEnv:
    
    
    def __init__(self, config_path: str, restore_step=None):
        
        self.env_config=read_yaml(config_path)
        self.restore_step_override = restore_step
        self.num_worker=self.env_config["num_worker"]
        self.manager=Manager()
        self.initinal_config(self.env_config)
        self.inference_communication = None
        self.inference_process = None
        if "inference" in self.env_config:
            inference_config = self.env_config["inference"]
            self.inference_communication = InferenceCommunication(self.num_worker)
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

        trainer1=get_class_by_name(self.config["trainer"])

        self.agent1:"BaseTrainer"=trainer1(self.config, restore_step, name="main")
        # Workers receive their initial model version through this channel.
        # Keep them aligned with `-r`, including the special latest value -1.
        self.info_communication.update_model(restore_step, restore_step)

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
    # sys.stdout = open(os.devnull, 'w')
    # sys.stderr = open(os.devnull, 'w')
    os.environ["RL_ROLLOUT_WORKER"] = "1"
    # The parent process owns Ctrl+C and performs coordinated shutdown.
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    # Each rollout is Python/CPU bound.  One torch thread per process avoids
    # OpenMP oversubscription when many environments run together.
    import torch
    torch.set_num_threads(env_config.get("rollout_torch_threads", 1))
    asyncio.run(
        run_parallel_room(
            env_config,
            info_communication,
            inference_communication,
            worker_id,
            room_class
        )
    )
