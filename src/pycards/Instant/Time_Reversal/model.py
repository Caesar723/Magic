
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Time_Reversal(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Time Reversal"

        self.type:str="Instant"

        self.mana_cost:str="5UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Undo all spells and effects from your opponent's last turn."
        self.image_path:str="cards/Instant/Time Reversal/image.jpg"



        