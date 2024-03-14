
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Verdant_Growth(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Verdant Growth"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Target creature gets +4/+4 until end of turn. If it's a Treefolk creature, it gains trample until end of turn."
        self.image_path:str="cards/Instant/Verdant Growth/image.jpg"



        