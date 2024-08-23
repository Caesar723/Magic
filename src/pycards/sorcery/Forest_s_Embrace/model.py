
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Forest_s_Embrace(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Forest's Embrace"

        self.type:str="Sorcery"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Search your library for up to three land cards, put them onto the battlefield tapped, then shuffle your library. "
        self.image_path:str="cards/sorcery/Forest's Embrace/image.jpg"



        