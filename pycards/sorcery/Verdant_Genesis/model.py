
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Verdant_Genesis(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Verdant Genesis"

        self.type:str="Sorcery"

        self.mana_cost:str="2G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Search your library for up to two land cards, put them onto the battlefield tapped, then shuffle your library. You may put a +1/+1 counter on each creature you control."
        self.image_path:str="cards/sorcery/Verdant Genesis/image.jpg"



        