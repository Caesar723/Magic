
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Mystic_Reversal(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Reversal"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. If that spell is countered this way, its controller may cast it without paying its mana cost during their next turn."
        self.image_path:str="cards/Instant/Mystic Reversal/image.jpg"



        