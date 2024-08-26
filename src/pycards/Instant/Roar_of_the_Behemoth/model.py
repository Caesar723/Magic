
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Roar_of_the_Behemoth(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Roar of the Behemoth"

        self.type:str="Instant"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="All enemy creatures get 0 power until the end of this turn."
        self.image_path:str="cards/Instant/Roar of the Behemoth/image.jpg"



        