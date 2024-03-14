
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery


class Fiery_Burst(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Fiery Burst"

        self.type:str="Sorcery"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Fiery Burst deals 2 damage to target creature or player."
        self.image_path:str="cards/sorcery/Fiery Burst/image.jpg"



        