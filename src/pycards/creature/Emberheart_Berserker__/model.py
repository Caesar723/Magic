
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import StateBuff
from pycards.land.Mountain.model import Mountain

class Emberheart_Berserker__(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Emberheart Berserker"
        self.live:int=2
        self.power:int=3
        self.actual_live:int=2
        self.actual_power:int=3

        self.type_creature:str="Human"
        self.type:str="Creature"

        self.mana_cost:str="1RR"
        self.color:str="colorless"
        self.type_card:str="Human"
        self.rarity:str="Common"
        self.content:str="Whenever Emberheart Berserker defends, it gets +0/+1 until end of turn for each Mountain you control."
        self.image_path:str="cards/creature/Emberheart Berserker  /image.jpg"


    def when_start_defend(self, card: "Creature | Player", player: "Player" = None, opponent: "Player" = None):
        for land in player.land_area:
            if isinstance(land,Mountain):
                buff=StateBuff(self,self,0,1)
                buff.set_end_of_turn()
                self.gain_buff(buff,self)
                


        return super().when_start_defend(card, player, opponent)


