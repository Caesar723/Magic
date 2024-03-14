
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Sacred_Reinforcement(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Sacred Reinforcement"

        self.type:str="Instant"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Tap up to two target creatures. They gain +1/+1 until end of turn."
        self.image_path:str="cards/Instant/Sacred Reinforcement/image.jpg"



        