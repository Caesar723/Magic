
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery


class Call_of_the_Tides(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Call of the Tides"

        self.type:str="Sorcery"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Draw two cards, then discard a card."
        self.image_path:str="cards/sorcery/Call of the Tides/image.jpg"



        