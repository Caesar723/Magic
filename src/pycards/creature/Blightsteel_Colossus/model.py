
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import Infect,Indestructible

class Blightsteel_Colossus(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Blightsteel Colossus"
        self.live:int=11
        self.power:int=11
        self.actual_live:int=11
        self.actual_power:int=11

        self.type_creature:str="Artifact Creature - Golem"
        self.type:str="Creature"

        self.mana_cost:str="12"
        self.color:str="colorless"
        self.type_card:str="Artifact Creature - Golem"
        self.rarity:str="Mythic Rare"
        self.content:str="Trample, Infect (This creature deals damage to creatures in the form of -1/-1 counters and to players in the form of poison counters.), Indestructible (This creature can't be destroyed by damage or effects that say \"destroy.\")"
        self.image_path:str="cards/creature/Blightsteel Colossus/image.jpg"

        self.flag_dict["Trample"]=True

        buff_infect=Infect(self,self)
        self.gain_buff(buff_infect,self)

        buff_indestructible=Indestructible(self,self)
        self.gain_buff(buff_indestructible,self)


        