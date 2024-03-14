
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Celestial_Intervention(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Intervention"

        self.type:str="Instant"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until end of turn, creatures you control gain indestructible. You may draw a card."
        self.image_path:str="cards/Instant/Celestial Intervention/image.jpg"



        