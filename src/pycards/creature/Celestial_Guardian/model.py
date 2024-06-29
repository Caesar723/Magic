
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Celestial_Guardian(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Celestial Guardian"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Angel Creature"
        self.type:str="Creature"

        self.mana_cost:str="3W"
        self.color:str="gold"
        self.type_card:str="Angel Creature"
        self.rarity:str="Rare"
        self.content:str="Flying, Vigilance"
        self.image_path:str="cards/creature/Celestial Guardian/image.jpg"



        