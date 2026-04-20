import sys
if __name__=="__main__":

    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    

import random
import asyncio
import os

from game.rlearning.utils.model import get_class_by_name
from game.rlearning.utils.file import read_yaml
from initinal_file import ORGPATH
from torch.multiprocessing import Queue,Manager,Process
from queue import Full, Empty
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.rlearning.communicate.training_parallel_room import Info_Communication
    from game.rlearning.utils.baseAgent import BaseTrainer

class BaseParallelEnv:
    
    
    def __init__(self,config_path:str):
        
        self.env_config=read_yaml(config_path)
        self.num_worker=self.env_config["num_worker"]
        self.manager=Manager()
        self.initinal_config(self.env_config)
        
        

    def initinal_config(self,config:dict):
        
        self.info_communication:"Info_Communication"=get_class_by_name(self.env_config["info_communication"])(self.env_config,self.manager)

        self.room_class=get_class_by_name(config["room"])
        agent_config=config["agent_config"]
        self.config_path=f"{ORGPATH}/{agent_config}"
        self.config=read_yaml(self.config_path)

        trainer1=get_class_by_name(self.config["trainer"])

        self.agent1:"BaseTrainer"=trainer1(self.config,self.config["restore_step"],name="main")

    def start_worker(self):
        self.worker_process=[Process(target=worker_process, args=(self.env_config, self.info_communication, i,self.room_class)) for i in range(self.num_worker)]
        for i in range(self.num_worker):
            self.worker_process[i].start()

        

    def run(self):
        pass

async def run_parallel_room(
    env_config,
    info_communication,
    worker_id:int,
    room_class:type):
    
    room=room_class(
        env_config,
        info_communication,
        worker_id
    )
    
    await room.game_start()
    await room.action_process_system()

def worker_process(
    env_config, 
    info_communication, 
    worker_id:int,
    room_class:type):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    asyncio.run(
        run_parallel_room(
            env_config,
            info_communication,
            worker_id,
            room_class
        )
    )
