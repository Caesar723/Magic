
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Wild_Growth(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Wild Growth"

        self.type:str="Instant"

        self.mana_cost:str="G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Search your library for a basic land card and put it onto the battlefield tapped, then shuffle your library."
        self.image_path:str="cards/Instant/Wild Growth/image.jpg"



        