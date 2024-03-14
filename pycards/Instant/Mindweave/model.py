
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Mindweave(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mindweave"

        self.type:str="Instant"

        self.mana_cost:str="UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell unless its controller pays X. If that spell is countered this way, you may draw X cards."
        self.image_path:str="cards/Instant/Mindweave/image.jpg"



        