
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Natural_Harmony(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Natural Harmony"

        self.type:str="Sorcery"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Search your library for a basic land card and put it onto the battlefield tapped, then shuffle your library. You gain 2 life."
        self.image_path:str="cards/sorcery/Natural Harmony/image.jpg"



        