
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Celestial_Herald(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Herald"
        self.live:int=3
        self.power:int=3

        self.type_creature:str="Angel Creature"
        self.type:str="Creature"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Angel Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="Flying, Lifelink. At the beginning of your upkeep, you may exile target nonland permanent. Return that permanent to the battlefield under its owner's control at the beginning of the next end step."
        self.image_path:str="cards/creature/Celestial Herald/image.jpg"



        