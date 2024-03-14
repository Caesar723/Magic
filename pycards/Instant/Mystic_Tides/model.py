
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Mystic_Tides(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Tides"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Counter target creature spell unless its controller pays 2."
        self.image_path:str="cards/Instant/Mystic Tides/image.jpg"



        