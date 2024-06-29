
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Arcane_Intervention(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Arcane Intervention"

        self.type:str="Instant"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Return target permanent to its owner's hand. Draw a card."
        self.image_path:str="cards/Instant/Arcane Intervention/image.jpg"



        