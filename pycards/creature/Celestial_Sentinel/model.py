
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature


class Celestial_Sentinel(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Sentinel"
        self.live:int=3
        self.power:int=3

        self.type_creature:str="Angel Creature"
        self.type:str="Creature"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Angel Creature"
        self.rarity:str="Rare"
        self.content:str="Flying, Vigilance"
        self.image_path:str="cards/creature/Celestial Sentinel/image.jpg"



        