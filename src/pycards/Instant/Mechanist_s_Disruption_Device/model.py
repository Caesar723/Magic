
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Mechanist_s_Disruption_Device(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mechanist's Disruption Device"

        self.type:str="Instant"

        self.mana_cost:str="3U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target spell. Then, create a token that's a copy of each artifact creature you control."
        self.image_path:str="cards/Instant/Mechanist's Disruption Device/image.jpg"



        