import torch
import asyncio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.room import Room
from game.type_action.actions import List_Action_Processor
from game.ppo_train import Agent_PPO
from game.agent import Agent_Player_Red
from game.player import Player

class Agent_Train_Red(Agent_Player_Red):

    def __init__(self, name: str,room:"Room",agent:Agent_PPO) -> None:
        decks_detail="Eternal Phoenix+Creature+4|Raging Firekin+Creature+4|Emberheart Salamander+Creature+4|Arcane Inferno+Instant+4|Pyroblast Surge+Instant+4|Fiery Blast+Instant+4|Inferno Titan+Creature+4|Flame Tinkerer+Creature+4|Mountain+Land+24"
        self.id_dict={}
        Player.__init__(self,name, decks_detail,room)
        self.agent=agent
        self.select_content:str=f'{name}|cancel'
        #self.data_counter=0
        self.notify_reward=True
        self.condition_reward=asyncio.Condition()
        


    async def beginning_phase(self):
        #print("test")
        result=await super().beginning_phase()
        
        async with self.condition_reward:
            self.notify_reward=True
            self.condition_reward.notify()
        
        return result
    
    async def store_data(self,state,action,reward_func):
        #print("wait")
        async with self.condition_reward:
            while not self.notify_reward:
              await self.condition_reward.wait()
        #print("end")

        
        next_state,reward,done=await reward_func()
        #print(reward,action,done)
        #print(reward,next_state,done)

        self.agent.store(state,action,reward,next_state,done)
        # if len(self.agent.reward)>=1024:
        #     print("____________________update agent____________________")
        #     self.update()
            


    def update(self):
        self.agent.train()

    