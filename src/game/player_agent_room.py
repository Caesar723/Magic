if __name__=="__main__":
    import sys
    from pathlib import Path
    src_root = next(parent for parent in Path(__file__).resolve().parents if parent.name == "src")
    if str(src_root) not in sys.path:
        sys.path.append(str(src_root))
    
   

#from room_server import RoomServer
import numpy as np
import asyncio
#from game.train_agent import Agent_Train_Red as Agent_Train
from game.room import Room
from game.player import Player
from game.agent import Agent_Player as Agent
import torch
import random
from torch import nn
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.base_agent_room import Base_Agent_Room
from game.action_validator import validate_player_action
from game.game_recorder import GameRecorder
from game.game_function_tool import ORGPATH

class PVE_Room(Base_Agent_Room):
    """
    当回合开始的时候，向那个活跃的agent发送做动作的请求
    做好一个动作之后把状态奖励等放入agent里
    直到agent 做出了 0:end turn的这个动作
    """

    def __init__(self,players:list[tuple],room_server) -> None:
        self.agent_response_running=False
        self.agent_response_pending=0
        self.agent_follow_up=False
        super().__init__(players,room_server)


        self.action_process_condition=asyncio.Condition()#等待直到agent_cache不是空
        self.agent_cache=[]
         #store current player which is in his turn
        self.active_player:"Agent|Player"#进行操作的玩家
        self.non_active_player:"Agent|Player"

    def choose_agent_config(self):
        agents=[
            f"{ORGPATH}/game/rlearning/weights/white/ppo_lstm2.yaml",
            f"{ORGPATH}/game/rlearning/weights/green/ppo_lstm3.yaml",
            f"{ORGPATH}/game/rlearning/weights/white2/ppo_lstm3.yaml",
        ]
        return random.choice(agents)

    def initinal_player(self,players:list[tuple]):
        #agents_deck="Eternal Phoenix+Creature+4|Raging Firekin+Creature+4|Emberheart Salamander+Creature+4|Arcane Inferno+Instant+4|Pyroblast Surge+Instant+4|Fiery Blast+Instant+4|Inferno Titan+Creature+4|Flame Tinkerer+Creature+4|Mountain+Land+24"

        # Agent_para=[(agents_deck,"Agent1")]
        print(self.stack,"test")
        self.player_1,self.player_2=Agent("Agent1",self,self.choose_agent_config()),\
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
        self.basic_func={
            "Agent1":self.initinal_function(self.player_1.config),
        }
        print(self.game_recorder,"test")


    async def message_receiver(self,message:str):
        base_message=message.split("||",1)[0]
        username,action_type,_=base_message.split("|",2)
        player=self.players[username]
        agent_message=username=="Agent1" and action_type in self.message_process_dict
        if isinstance(player,Player) and not isinstance(player,Agent):
            valid,_=validate_player_action(self,message)
            if valid and player.opponent.name in self.basic_func:
                self.basic_func[player.opponent.name]["add_opponent_history"](player.opponent,player,message)
        elif agent_message:
            self.agent_response_pending+=1
        try:
            await super().message_receiver(message)
        except Exception:
            if agent_message and self.agent_response_pending>0:
                self.agent_response_pending-=1
            raise

    async def message_process(self):
        while self.gamming:
            if not self.message_process_queue:
                async with self.message_process_condition:
                    await self.message_process_condition.wait_for(lambda: len(self.message_process_queue)>0)
            func,args=self.message_process_queue.pop(0)
            username=args[0] if args else None
            completed=False
            try:
                await func(*args)
                await self.check_death()
                completed=True
            finally:
                if username=="Agent1" and self.agent_response_pending>0:
                    self.agent_response_pending-=1
            if completed and self.agent_response_pending==0 and self.agent_follow_up:
                self.agent_follow_up=False
                if self.gamming:
                    await self.ask_agent_do_act()


    async def process_action(self,agent:Agent,action:int)->tuple:
        #将action 处理生成动作并且传入房间，将其挂起，直到房间处理好请求收到结束信号
        #如果是攻击的action，给敌方agent发送动作请求，自己挂起再一次，直到地方action动作做好发送信息给自己，自己结束挂起，计算state
        # 获取state，done，计算reward
        #返回new state 和 reward 和 done
        message:str=await self.basic_func[agent.name]["num2action"](agent,action)
        await self.message_receiver(message)

        
        # username,type,content=message.split("|")
        # await self.message_process_dict[type](username,content)
        
        return 
    
    def get_flag(self,flag_name:str):
        key="{}_bullet_time_flag"
        enable_bullet_response=self.enable_agent_bullet_response()

        if flag_name==key.format("Agent1") and not enable_bullet_response:
            if not (super().get_flag("attacker_defenders") and self.attacker not in self.player_1.battlefield):
                return True

        return super().get_flag(flag_name)
    




    def enable_agent_bullet_response(self):
        return self.player_1.config.get("enable_bullet_response",False)


    def reset_bullet_pass(self):
        for player_name in self.players:
            self.flag_dict[f"{player_name}_bullet_time_flag"]=False

    async def request_agent_response(self,username,result,reset_bullet_pass=True):
        if username=="Agent1":
            return
        if result is not None and not result[0]:
            return
        if not self.get_flag("bullet_time") or not self.gamming:
            return
        if reset_bullet_pass:
            self.reset_bullet_pass()
        await self.ask_agent_do_act()



    async def continue_agent_action(self):
        if not self.gamming:
            return
        if self.agent_response_pending>0:
            self.agent_follow_up=True
            return
        await self.ask_agent_do_act()

    async def ask_agent_do_act(self):
        if not self.gamming or self.agent_response_running or self.agent_response_pending>0:
            return
        self.agent_response_running=True
        try:
            await asyncio.sleep(1)
            agent:Agent=self.player_1
            state=self.basic_func[agent.name]["get_state"](agent)
            mask=self.basic_func[agent.name]["create_action_mask"](agent)
            state["mask"]=mask
            print("state get")
            action=agent.choose_action(state,isTrain=False)
            print("action choose")
            return await self.process_action(agent,action)
        finally:
            self.agent_response_running=False

    async def play_card(self,username:str,content:str):
        result=await super().play_card(username,content)
        success=result is None or result[0]

        if success and username=="Agent1" and self.enable_agent_bullet_response():
            self.reset_bullet_pass()
        elif username!="Agent1" and self.enable_agent_bullet_response():
            await self.request_agent_response(username,result)

        return (True,"success") if result is None else result

    async def end_bullet_time(self):

        result= await super().end_bullet_time() 
        print(self.active_player.name)
        if self.active_player.name=="Agent1":
            await self.continue_agent_action()
        return result

    async def end_bullet(self,username:str,content:str):
        result=await super().end_bullet(username,content)
        if username!="Agent1" and result[0] and self.enable_agent_bullet_response() and self.get_flag("bullet_time"):
            await self.request_agent_response(username,result,reset_bullet_pass=False)
        return result
    
    async def select_attacker(self,username:str,content:str):
        result=await super().select_attacker(username,content)

        if username!="Agent1" and result[0]:
            await self.request_agent_response(username,result)
        elif username=="Agent1" and result[0] and self.enable_agent_bullet_response():
            self.reset_bullet_pass()

        return result
    
    async def end_turn_time(self):
        await super().end_turn_time()
        print(self.active_player.name)
        if self.active_player.name=="Agent1":
            await self.continue_agent_action()

    async def game_start(self):
        await super().game_start()
        if self.active_player.name=="Agent1":
            await self.continue_agent_action()

    async def select_defender(self,username:str,content:str):
        result=await super().select_defender(username,content)

        if username=="Agent1" and result[0]:
            if self.enable_agent_bullet_response():
                self.reset_bullet_pass()
            await self.message_receiver("Agent1|end_bullet|")
        elif self.enable_agent_bullet_response():
            await self.request_agent_response(username,result)

        return result

    async def activate_ability(self,username:str,content:str):
        result=await super().activate_ability(username,content)
        if username=="Agent1" and result[0]:
            await self.continue_agent_action()
        return result







        





            

    












