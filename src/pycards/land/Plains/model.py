
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.game_function_tool import select_object


class Plains(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Plains"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="gold"
        self.type_card:str="Land"
        self.rarity:str="Uncommon"
        self.content:str=""
        self.image_path:str="cards/land/Plains/image.jpg"


    def generate_mana(self) -> dict:
        return {"W":1}
        