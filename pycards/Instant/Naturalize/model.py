
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Naturalize(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Naturalize"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Destroy target artifact or enchantment."
        self.image_path:str="cards/Instant/Naturalize/image.jpg"



        