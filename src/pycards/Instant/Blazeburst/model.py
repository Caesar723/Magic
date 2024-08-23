
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Blazeburst(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Blazeburst"

        self.type:str="Instant"

        self.mana_cost:str="1RR"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Blazeburst deals 3 damage to any target."
        self.image_path:str="cards/Instant/Blazeburst/image.jpg"



        