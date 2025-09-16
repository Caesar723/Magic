import random
import torch
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.room import Room
from game.type_action.actions import List_Action_Processor
from game.ppo_train import Agent_PPO
from game.player import Player
from initinal_file import CARD_DICTION
from game.game_function_tool import ORGPATH
from game.rlearning.utils.file import read_yaml
from game.rlearning.utils.model import get_class_by_name





class Agent_Player_Red(Player):

    def __init__(self, name: str,room:"Room",config_path:str=f"{ORGPATH}/game/rlearning/config/white/ppo_lstm2.yaml") -> None:
        self.config=read_yaml(config_path)
        decks_detail=self.config["cards"]
        self.id_dict={}
        super().__init__(name, decks_detail, room)

        self.action_history=[0]
        self.action_history_length=self.config.get("action_history_length",1)

        
        model_class=get_class_by_name(self.config["trainer"])
        self.agent=model_class(self.config,self.config["restore_step"],name="agent1")
        self.select_content:str=f'{name}|cancel'
                
    def choose_action(self,state,isTrain=False):
        action=self.agent.choose_action([state],isTrain=isTrain)["action"]
        if action==0:
            self.add_action_history(action)
        elif action==1:
            pass
        elif action>=2 and action<=11:
            self.add_action_history(action-1)
        elif action>=12 and action<=21:
            self.add_action_history(action-1)
        else:
            history_action=22+((action-22)//33)
            self.add_action_history(history_action-1)

        return action
    def add_action_history(self,action:int):
        self.action_history.append(action)
        if len(self.action_history)>self.action_history_length:
            self.action_history.pop(0)

    def get_action_history(self):
        return list(self.action_history)

    def clean_action_history(self):
        self.action_history=[0]
    
    def get_flag(self,flag_name:str):
        if flag_name=="game_over":
            return True
        if flag_name in self.flag_dict:
            return self.flag_dict[flag_name]
        else:
            return False
        

    def initinal_decks(self,decks_detail:str):#generate cards
        id_counter=1
        for element in decks_detail.split("|"):
            name,type,number=element.split("+")
            number=int(number)
            self.deck+=[CARD_DICTION[f"{name}_{type}"](self) for i in range(number)]

            key=f"{name}+{type}"
            if not key in self.id_dict:
                self.id_dict[key]=id_counter
                id_counter+=1
        random.shuffle(self.deck)
        self.hand=self.deck[:7]# get 7 card to hand
        self.library=self.deck[7:]# the rest is in the library

    async def send_text(self, message):
        return 
    

    async def send_selection_cards(self,selected_cards:list,selection_random:bool=False):
        async with self.selection_lock:
            # cards=','.join([card.text(self,False) for card in selected_cards])
            # await self.send_text(f"select(cards,parameters({cards}))")

            data =self.select_content#await self.receive_text()# 玩家｜cards｜index
            selected_card=self.get_object(selected_cards,data)
        
        if selected_card=="cancel" and selection_random:
            if selected_cards:
                selected_card=random.choice(selected_cards)
            #await self.send_text("end_select()")
        return selected_card
    
    async def receive_text(self):
        
        return self.select_content
    
    def set_select_content(self,content:str):
        self.select_content=content


    

        