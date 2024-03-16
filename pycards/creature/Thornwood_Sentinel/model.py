
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Thornwood_Sentinel(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Thornwood Sentinel"
        self.live:int=3
        self.power:int=2
        self.actual_live:int=3
        self.actual_power:int=2

        self.type_creature:str="Elemental Creature"
        self.type:str="Creature"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Elemental Creature"
        self.rarity:str="Common"
        self.content:str="Reach (This creature can block creatures with flying)"
        self.image_path:str="cards/creature/Thornwood Sentinel/image.jpg"



        