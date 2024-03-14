
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Flames_of_Fury(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Flames of Fury"

        self.type:str="Instant"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Flames of Fury deals 3 damage to any target. If a creature dealt damage this way would die this turn, exile it instead."
        self.image_path:str="cards/Instant/Flames of Fury/image.jpg"



        