
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Tidal_Sprite(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Tidal Sprite"
        self.live:int=1
        self.power:int=1
        self.actual_live:int=1
        self.actual_power:int=1

        self.type_creature:str="Merfolk Creature"
        self.type:str="Creature"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Merfolk Creature"
        self.rarity:str="Common"
        self.content:str="Flying (This creature can't be blocked except by creatures with flying or reach.)"
        self.image_path:str="cards/creature/Tidal Sprite/image.jpg"

        self.flag_dict["flying"]=True
        



