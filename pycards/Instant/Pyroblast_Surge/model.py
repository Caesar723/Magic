
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Pyroblast_Surge(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Pyroblast Surge"

        self.type:str="Instant"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Pyroblast Surge deals 3 damage to target creature or player. If you control a Mountain, Pyroblast Surge deals 1 additional damage."
        self.image_path:str="cards/Instant/Pyroblast Surge/image.jpg"



        