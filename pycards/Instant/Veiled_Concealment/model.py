
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Veiled_Concealment(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Veiled Concealment"

        self.type:str="Instant"

        self.mana_cost:str="U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Target creature is unblockable until end of turn. Draw a card."
        self.image_path:str="cards/Instant/Veiled Concealment/image.jpg"



        