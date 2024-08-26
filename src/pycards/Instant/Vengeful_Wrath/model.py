
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Vengeful_Wrath(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Vengeful Wrath"

        self.type:str="Instant"

        self.mana_cost:str="3BB"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="When your creature dies, deal damage equal to its power to target opponent's creature."
        self.image_path:str="cards/Instant/Vengeful Wrath/image.jpg"



        