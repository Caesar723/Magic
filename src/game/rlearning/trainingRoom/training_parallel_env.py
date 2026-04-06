import sys
if __name__=="__main__":

    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    

import random
import asyncio
import os

from game.rlearning.utils.model import get_class_by_name
from game.rlearning.utils.file import read_yaml
from initinal_file import ORGPATH
from multiprocessing import Queue,Manager,Process
from queue import Full, Empty

class Info_Communication:
    def __init__(self,num_worker:int,manager):
        self.data_queue = Queue(maxsize=20)
        self.num_worker = num_worker
        self.communication={key:manager.dict() for key in range(num_worker)}

    def store_game_date(self,data:list[dict]):
        try:
            self.data_queue.put(data, block=False)
        except Full:
            try:
                self.data_queue.get(block=False)
            except Empty:
                pass
            self.data_queue.put(data, block=False)

    def get_game_date(self):
        return self.data_queue.get()


    def check_model_update(self,worker_id:int):
        return self.communication[worker_id].get("model_update",False)
            
    def get_model_info(self,worker_id:int):

        result={
            
            "success_update":self.communication[worker_id].get("model_update",False),
            "model_update_steps":self.communication[worker_id].get("model_update_steps",0),
            "model_path":self.communication[worker_id].get("model_path",None),

            "success_opponent_update":self.communication[worker_id].get("model_opponent_update",False),
            "config_opponent_path":self.communication[worker_id].get("config_opponent_path",None),
            "model_opponent_path":self.communication[worker_id].get("model_opponent_path",None),
        }
        self.communication[worker_id]["model_update"]=False
        self.communication[worker_id]["model_opponent_update"]=False
        return result


    def update_model(self,steps,model_path:str):
        for worker_id in range(self.num_worker):
            self.communication[worker_id]["model_update"]=True
            self.communication[worker_id]["model_update_steps"]=steps
            self.communication[worker_id]["model_path"]=model_path

    def update_model_opponent(self,worker_id:int,config_opponent_path:str,model_path:str):
        self.communication[worker_id]["model_opponent_update"]=True
        self.communication[worker_id]["config_opponent_path"]=config_opponent_path
        self.communication[worker_id]["model_opponent_path"]=model_path


class Parallel_Env:
    
    
    def __init__(self,config_path:str):
        
        self.env_config=read_yaml(config_path)
        self.num_worker=self.env_config["num_worker"]
        self.initinal_config(self.env_config)
        self.manager=Manager()
        self.info_communication=Info_Communication(self.num_worker,self.manager)
        self.info_communication.update_model(0,0)
        for i in range(self.num_worker):
            self.info_communication.update_model_opponent(
                i,
                random.choice(self.config_path_list),
                0
            )

    def initinal_config(self,config:dict):
        self.room_class=get_class_by_name(config["room"])
        agent_config=config["agent_config"]
        opponent_configs=config["opponent_config"]
        self.config_path=f"{ORGPATH}/{agent_config}"
        self.config_path_list=[f"{ORGPATH}/{opponent_config}" for opponent_config in opponent_configs]
        self.config=read_yaml(self.config_path)
        self.config_list=[read_yaml(config_path) for config_path in self.config_path_list]

        trainer1=get_class_by_name(self.config["trainer"])

        self.agent1=trainer1(self.config,self.config["restore_step"],name="main")

    def start_worker(self):
        self.worker_process=[Process(target=worker_process, args=(self.config_path, self.config_path_list, self.info_communication, i,self.room_class)) for i in range(self.num_worker)]
        for i in range(self.num_worker):
            self.worker_process[i].start()

    def run(self):


        while True:
            data=self.info_communication.get_game_date()
            self.agent1.store_round_data(data)

            is_update=self.agent1.update()
            if is_update:
                self.info_communication.update_model(self.agent1.step,-1)

async def run_parallel_room(
    config_path:str,
    config_path_list:list,
    info_communication:"Info_Communication",
    worker_id:int,
    room_class:type):
    
    room=room_class(
        config_path,
        config_path_list,
        info_communication,
        worker_id
    )
    
    await room.game_start()
    await room.action_process_system()

def worker_process(
    config_path:str, 
    config_path_list:list, 
    info_communication:"Info_Communication", 
    worker_id:int,
    room_class:type):
    # sys.stdout = open(os.devnull, 'w')
    # sys.stderr = open(os.devnull, 'w')
    asyncio.run(
        run_parallel_room(
            config_path,
            config_path_list,
            info_communication,
            worker_id,
            room_class
        )
    )


if __name__=="__main__":

    env=Parallel_Env(
        config_path="/Users/xuanpeichen/Desktop/code/python/openai/src/game/rlearning/config/parallel/parallel_specific_v1.yaml",
    )
    env.start_worker()
    env.run()