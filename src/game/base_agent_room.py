
if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
   

#from room_server import RoomServer
import numpy as np
import asyncio
import importlib
from functools import partial

from game.agent import Agent_Player as Agent
from game.room import Room
from game.rlearning.module.ppo_agent import PPOTrainer
from game.rlearning.utils.model import get_class_by_name

from game.card import Card
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.rlearning.utils.file import read_yaml








class Base_Agent_Room(Room):


    def __init__(self,players:list[tuple],room_server) -> None:#((deck,user_name1),...)

        super().__init__(players,room_server)

    def initinal_function(self,config:dict):
        result={}
        get_reward=get_class_by_name(config.get("reward_function","game.rlearning.rewards.win_base.get_reward"))
        result["get_reward"]=partial(get_reward,self)

        get_state=get_class_by_name(config.get("state_function","game.rlearning.states.single_deck.get_state"))
        result["get_state"]=partial(get_state,self)


        num2action=get_class_by_name(config.get("action_transform_function","game.rlearning.actions.single_deck.num2action"))
        result["num2action"]=partial(num2action,self)

        create_action_mask=get_class_by_name(config.get("action_mask_function","game.rlearning.actions.single_deck.create_action_mask"))
        result["create_action_mask"]=partial(create_action_mask,self)

        return result



    
    async def check_player_die(self):
        died_player=[]
        for name in self.players:
            if (await self.players[name].check_dead()):
                died_player.append(self.players[name])
        return bool(died_player)


    def get_card_special_types(self,card:Card):
        special_types=np.zeros(20)

        card_type=0

        if isinstance(card,Creature):
            card_type=1
            if not (Creature.when_enter_battlefield is card.when_enter_battlefield.__func__):
                special_types[0]=1
            if not (Creature.when_leave_battlefield is card.when_leave_battlefield.__func__):
                special_types[1]=1
        elif isinstance(card,Instant):
            card_type=2
            if not (Instant.card_ability is card.card_ability.__func__):
                special_types[0]=1
        elif isinstance(card,Land):
            card_type=3
            if not (Land.when_enter_landarea is card.when_enter_landarea.__func__):
                special_types[0]=1
            if not (Land.when_enter_landarea is card.when_enter_landarea.__func__):
                special_types[1]=1
        elif isinstance(card,Sorcery):
            card_type=4
            if not (Sorcery.card_ability is card.card_ability.__func__):
                special_types[0]=1
            
            
        for i,flag in enumerate(["reach","Trample","flying","haste","Flash","lifelink"]):
            if card.get_flag(flag):
                special_types[2+i]=1

        if not card.get_flag("tap") and not card.get_flag("summoning_sickness"):
            special_types[8]=1
        return card_type,special_types

    def get_time_state(self):
        return np.array([0,1] if self.get_flag("attacker_defenders") else [1,0])
    
    def get_attacker(self):
        if self.get_flag("attacker_defenders"):
            result=list(self.attacker.state)
        else:
            result=[0,0]
        result=np.array(result)/10
        return result


    def get_cost_total(self,agent:Agent):
        player_mana=dict(agent.mana)
        for land in agent.land_area:
            if not land.get_flag("tap"):
                mana=land.generate_mana()
                for key in mana:
                    player_mana[key]+=mana[key]
        return player_mana


        


    async def initinal_environmrnt(self):# 返回一个state和评分
        self.turn_timer:int=0
        self.max_turn_time:int=120

        #used to count the time when player use instant and in bullet_time
        self.bullet_timer:int=0
        self.max_bullet_time:int=10


        #used to store the each flag like whether is bullet_time
        self.flag_dict:dict={}

        #used to store each counter like number of turns
        self.counter_dict:dict={}

        self.stack:list[tuple]=[]
        self.attacker:Creature=None
        # for task in self.tasks:
        #     task.cancel()
        self.tasks=[]
        self.initinal_player(None,is_initinal=False)


        for recorder_key in self.game_recorder:
            recorder=self.game_recorder[recorder_key]
            player=self.players[recorder_key]
            await recorder.save_binary(base_path=player.agent.logdir,extra_info=str(player.agent.step))
            #print(recorder.save_flag)

        self.action_store_list=[]
        if self.update_flag[self.player_1.name]:
            self.update_flag[self.player_1.name]=False
            self.update_flag[self.player_2.name]=False
            for recorder_key in self.game_recorder:
                self.game_recorder[recorder_key].reset_save_flag(self.players[recorder_key])
        
        await self.game_start()


    def create_sort_function(self,agent:Agent):
        def sort_function(card:Creature):
            score=self.get_creature_reward(card)
            if agent.agent.config.get("sort_method","score")=="score_tap":
                if (not card.get_flag("summoning_sickness") or card.get_flag("haste")) and\
                not card.get_flag("tap") and (card.get_counter_from_dict("attack_counter")>0):
                    score+=100
            return score
        return sort_function


    def get_creature_reward(self,card:Creature,in_battle:bool=False):
        if (card.get_flag("tap") or card.get_flag("summoning_sickness")) and not in_battle:
            p,d=card.power,card.live

            if p<=0 or d<=0:
                return 0
            state1=(p+d)/2
            state2=(p*d)**0.5
            r_state=(state1+state2)/12
            return r_state+0.05
        p,d=card.state[0],card.state[1]
        if p<=0 or d<=0:
            return 0
        state1=(p+d)/2
        state2=(p*d)**0.5
        r_state=(state1+state2)/10
        for flag in ["reach","Trample","flying","haste","Flash","lifelink"]:
            if card.get_flag(flag):
                r_state*=1.1
        return r_state+0.05
