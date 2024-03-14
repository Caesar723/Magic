
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Fiery_Blast(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Fiery Blast"

        self.type:str="Instant"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Fiery Blast deals 2 damage to any target."
        self.image_path:str="cards/Instant/Fiery Blast/image.jpg"



        