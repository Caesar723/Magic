
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Avenging_Light(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Avenging Light"

        self.type:str="Instant"

        self.mana_cost:str="3W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Exile target nonland permanent. If it was a creature, you gain life equal to its power."
        self.image_path:str="cards/Instant/Avenging Light/image.jpg"



        