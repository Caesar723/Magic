
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.game_function_tool import select_object


class Island(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Island"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="blue"
        self.type_card:str="Land"
        self.rarity:str="Uncommon"
        self.content:str=""
        self.image_path:str="cards/land/Island/image.jpg"



        