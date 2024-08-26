
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Divine_Sanctuary(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Divine Sanctuary"

        self.type:str="Instant"

        self.mana_cost:str="4WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until the start of your next turn, you and all creatures you control gain immunity to all effects."
        self.image_path:str="cards/Instant/Divine Sanctuary/image.jpg"



        