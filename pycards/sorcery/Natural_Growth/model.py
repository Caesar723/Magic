
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery


class Natural_Growth(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Natural Growth"

        self.type:str="Sorcery"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Target creature gets +2/+2 until end of turn."
        self.image_path:str="cards/sorcery/Natural Growth/image.jpg"



        