
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Merfolk_Wayfinder(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Merfolk Wayfinder"
        self.live:int=1
        self.power:int=1
        self.actual_live:int=1
        self.actual_power:int=1

        self.type_creature:str="Merfolk Creature"
        self.type:str="Creature"

        self.mana_cost:str="U"
        self.color:str="blue"
        self.type_card:str="Merfolk Creature"
        self.rarity:str="Common"
        self.content:str="Whenever Merfolk Wayfinder enters the battlefield, you may scry 1. (Look at the top card of your library. You may put that card on the bottom of your library.)"
        self.image_path:str="cards/creature/Merfolk Wayfinder/image.jpg"



        