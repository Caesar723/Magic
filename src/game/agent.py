import random
import torch

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.room import Room
from game.type_action.actions import List_Action_Processor
from game.ppo_train import Agent_PPO
from game.player import Player
from initinal_file import CARD_DICTION
from game.game_function_tool import ORGPATH



class Agent_Player_Red(Player):

    def __init__(self, name: str,room:"Room") -> None:
        decks_detail="Eternal Phoenix+Creature+4|Raging Firekin+Creature+4|Emberheart Salamander+Creature+4|Arcane Inferno+Instant+4|Pyroblast Surge+Instant+4|Fiery Blast+Instant+4|Inferno Titan+Creature+4|Flame Tinkerer+Creature+4|Mountain+Land+24"
        self.id_dict={}
        super().__init__(name, decks_detail, room)

        self.agent=Agent_PPO(271,352,train=False)
        self.agent.load_pth(
            f"{ORGPATH}/game/agent_pth/agent_red/model_complete_act.pth",
            f"{ORGPATH}/game/agent_pth/agent_red/model_complete_val.pth"
        )
        self.select_content:str=f'{name}|cancel'
                
    def choose_action(self,num_state,cards_id,mask:torch.Tensor=None):
        return self.agent.choose_act(num_state,cards_id,mask)
    
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


    

        