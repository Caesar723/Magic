
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Abyssal_Echoes(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Abyssal Echoes"

        self.type:str="Sorcery"

        self.mana_cost:str="5BB"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Search your library for a creature card with a mana value of 7 or greater and put it onto the battlefield."
        self.image_path:str="cards/sorcery/Abyssal Echoes/image.jpg"



        