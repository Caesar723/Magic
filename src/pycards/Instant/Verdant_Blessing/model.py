
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Verdant_Blessing(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Verdant Blessing"

        self.type:str="Instant"

        self.mana_cost:str="1GG"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Verdant Blessing allows you to search your library for a basic land card and put it onto the battlefield tapped. Then, shuffle your library."
        self.image_path:str="cards/Instant/Verdant Blessing/image.jpg"



        