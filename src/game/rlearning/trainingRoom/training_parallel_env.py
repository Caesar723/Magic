if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
   
import inspect
import traceback
#from room_server import RoomServer
import numpy as np
import asyncio
import random
import os
from game.train_agent import Agent_Train 
from game.room import Room
from game.ppo_train import Agent_PPO
from game.rlearning.module.ppo_agent import PPOTrainer
from game.rlearning.utils.model import get_class_by_name

from game.card import Card
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.rlearning.utils.file import read_yaml
from game.base_agent_room import Base_Agent_Room
from game.game_recorder import GameRecorder
from game.rlearning.utils.agentSchedule import AgentSchedule
from game.rlearning.trainingRoom.training_parallel_room import worker_process

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
    
    
    def __init__(self,num_worker:int,config_path:str,config_path_list:list):
        self.num_worker=num_worker
        self.config_path=config_path
        self.config_path_list=config_path_list
        self.config=read_yaml(config_path)
        self.config_list=[read_yaml(config_path) for config_path in config_path_list]

        trainer1=get_class_by_name(self.config["trainer"])
        #trainer_list=[get_class_by_name(config["trainer"]) for config in self.config_list]
        
        self.agent1=trainer1(self.config,self.config["restore_step"],name="main")
        # self.agent_list={
        #     config_path_list[i]:trainer(self.config_list[i],self.config_list[i]["restore_step"],name=f"agent{i+1}") 
        #     for i,trainer in enumerate(trainer_list)
        # }
        self.manager=Manager()
        self.info_communication=Info_Communication(num_worker,self.manager)
        self.info_communication.update_model(0,0)
        for i in range(num_worker):
            self.info_communication.update_model_opponent(
                i,
                random.choice(self.config_path_list),
                0
            )

    def start_worker(self):
        self.worker_process=[Process(target=worker_process, args=(self.config_path, self.config_path_list, self.info_communication, i)) for i in range(self.num_worker)]
        for i in range(self.num_worker):
            self.worker_process[i].start()

    def run(self):


        while True:
            data=self.info_communication.get_game_date()
            self.agent1.store_round_data(data)

            is_update=self.agent1.update()
            if is_update:
                self.info_communication.update_model(self.agent1.step,-1)


if __name__=="__main__":
    env=Parallel_Env(5,
        "/Users/xuanpeichen/Desktop/code/python/openai/src/game/rlearning/config/white/ppo_lstm3.yaml",
        [
        "/Users/xuanpeichen/Desktop/code/python/openai/src/game/rlearning/config/white/ppo_lstm2.yaml",
        ]
    )
    env.start_worker()
    env.run()