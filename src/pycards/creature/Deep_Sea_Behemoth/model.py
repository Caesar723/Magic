
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Deep_Sea_Behemoth(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Deep Sea Behemoth"
        self.live:int=7
        self.power:int=7
        self.actual_live:int=7
        self.actual_power:int=7

        self.type_creature:str="Creature - Leviathan"
        self.type:str="Creature"

        self.mana_cost:str="6UU"
        self.color:str="blue"
        self.type_card:str="Creature - Leviathan"
        self.rarity:str="Rare"
        self.content:str="Stealth. When Deep Sea Behemoth attacks, all opponent's creatures lose all abilities until end of turn."
        self.image_path:str="cards/creature/Deep Sea Behemoth/image.jpg"



        