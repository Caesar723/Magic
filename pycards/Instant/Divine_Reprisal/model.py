
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Divine_Reprisal(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Divine Reprisal"

        self.type:str="Instant"

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Destroy target attacking creature."
        self.image_path:str="cards/Instant/Divine Reprisal/image.jpg"



        