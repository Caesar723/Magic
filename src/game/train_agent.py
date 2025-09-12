import torch
import asyncio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.room import Room
from game.type_action.actions import List_Action_Processor
from game.rlearning.utils.baseAgent import BaseTrainer
from game.agent import Agent_Player_Red
from game.player import Player

class Agent_Train_Red(Agent_Player_Red):

    def __init__(self, name: str,room:"Room",agent:BaseTrainer) -> None:
        
        decks_detail=agent.config["cards"]
        self.id_dict={}
        Player.__init__(self,name, decks_detail,room)
        self.agent=agent
        self.select_content:str=f'{name}|cancel'
        #self.data_counter=0
        self.notify_reward=True
        self.condition_reward=asyncio.Condition()

        self.pedding_store_task=[]
        self.action_history=[0]
        self.action_history_length=agent.config.get("action_history_length",1)

        
    def add_pedding_store_task(self,task):
        self.pedding_store_task.append(task)
    async def clear_pedding_store_task(self):
        for task in self.pedding_store_task:
            await task()
        self.pedding_store_task=[]

    async def beginning_phase(self):
        #print("test")
        result=await super().beginning_phase()
        
        await self.clear_pedding_store_task()
        
        return result
    
    async def store_data(self,state,action,reward_func):
        
        
        # async with self.condition_reward:
        #     while not self.notify_reward:
        #         print("wait",action,id(state))
        #         await self.condition_reward.wait()
                #print("end",action,id(state))
        next_state,reward,done,global_reward=await reward_func()
        
        #print(reward,action,done)
        #print(reward,next_state,done)
       

        batch={
            "state":state,
            "action":action,
            "reward":reward,
            "next_state":next_state,
            "done":done,
            "global_reward":global_reward
        }
        #print(action,reward)

        self.agent.store(batch)
        # if len(self.agent.reward)>=1024:
        #     print("____________________update agent____________________")
        #     self.update()
            


    def update(self):
        self.agent.update()

    