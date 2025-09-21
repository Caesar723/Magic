if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
   

#from room_server import RoomServer
import numpy as np
import asyncio
#from game.train_agent import Agent_Train_Red as Agent_Train
from game.room import Room
from game.ppo_train import Agent_PPO
from game.player import Player
from game.agent import Agent_Player as Agent
import torch
from torch import nn
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.base_agent_room import Base_Agent_Room
from game.game_recorder import GameRecorder

class PVE_Room(Base_Agent_Room):
    """
    当回合开始的时候，向那个活跃的agent发送做动作的请求
    做好一个动作之后把状态奖励等放入agent里
    直到agent 做出了 0:end turn的这个动作
    """

    def __init__(self,players:list[tuple],room_server) -> None:
        #self.agent1=Agent_PPO(251,352)
        
        super().__init__(players,room_server)


        self.action_process_condition=asyncio.Condition()#等待直到agent_cache不是空
        self.agent_cache=[]
         #store current player which is in his turn
        self.active_player:"Agent|Player"#进行操作的玩家
        self.non_active_player:"Agent|Player"

        

    def initinal_player(self,players:list[tuple]):
        #agents_deck="Eternal Phoenix+Creature+4|Raging Firekin+Creature+4|Emberheart Salamander+Creature+4|Arcane Inferno+Instant+4|Pyroblast Surge+Instant+4|Fiery Blast+Instant+4|Inferno Titan+Creature+4|Flame Tinkerer+Creature+4|Mountain+Land+24"

        # Agent_para=[(agents_deck,"Agent1")]
        print(self.stack,"test")
        self.player_1,self.player_2=Agent("Agent1",self),\
                                    Player(players[0][1],players[0][0],self)
        self.player_1.set_opponent_player(self.player_2,self)
        self.player_2.set_opponent_player(self.player_1,self)
        self.players:dict={
            "Agent1":self.player_1,
            players[0][1]:self.player_2
        }

        self.players_socket:dict={
            "Agent1":None,
            players[0][1]:None
        }
        self.game_recorder:dict["GameRecorder"]={
            "Agent1":GameRecorder(self.player_1,self),
            players[0][1]:GameRecorder(self.player_2,self)
        }
        print(self.game_recorder,"test")




    async def process_action(self,agent:Agent,action:int)->tuple:
        #将action 处理生成动作并且传入房间，将其挂起，直到房间处理好请求收到结束信号
        #如果是攻击的action，给敌方agent发送动作请求，自己挂起再一次，直到地方action动作做好发送信息给自己，自己结束挂起，计算state
        # 获取state，done，计算reward
        #返回new state 和 reward 和 done
        message:str=await self.num2action(agent,action)
        print(message)
        print(self)
        print(self.get_reward_attack(agent)["reward"])

        await self.message_receiver(message)

        
        # username,type,content=message.split("|")
        # await self.message_process_dict[type](username,content)
        
        return 
    
    def get_flag(self,flag_name:str):
        key="{}_bullet_time_flag"
        if flag_name==key.format("Agent1") and not (self.get_flag('attacker_defenders') and not self.attacker in self.player_1.battlefield):
            return True
        if flag_name in self.flag_dict:
            
            return self.flag_dict[flag_name]
        else:
            return False
    




        






    async def ask_agent_do_act(self):
        await asyncio.sleep(1)
        agent:Agent=self.player_1
        state=self.get_new_state(agent)
        mask=self.create_action_mask(agent)
        state["mask"]=mask
        print("state get")
        action=agent.choose_action(state,isTrain=False)
        print("action choose")
        # print(action)
        return await self.process_action(agent,action)


    async def end_bullet_time(self):

        result= await super().end_bullet_time() 
        print(self.active_player.name)
        if self.active_player.name=="Agent1":
            await self.ask_agent_do_act()
        return result
    
    async def select_attacker(self, username: str, content: str):
        result=await super().select_attacker(username, content)
        if username!="Agent1" and result[0]:
            print(await self.ask_agent_do_act())
        return result
    
    async def end_turn_time(self):
        await super().end_turn_time()
        print(self.active_player.name)
        if self.active_player.name=="Agent1":
            await self.ask_agent_do_act()

    async def game_start(self):
        await super().game_start()
        if self.active_player.name=="Agent1":
            await self.ask_agent_do_act()

    async def select_defender(self, username: str, content: str):
        result= await super().select_defender(username, content)
        if username=="Agent1":
            await self.message_receiver("Agent1|end_bullet|")
            
        return result
         







        





            

    















