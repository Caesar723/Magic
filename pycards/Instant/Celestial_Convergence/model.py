
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Celestial_Convergence(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Convergence"

        self.type:str="Instant"

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Exile target permanent. If that permanent's mana value is 3 or less, its controller gains life equal to its mana value."
        self.image_path:str="cards/Instant/Celestial Convergence/image.jpg"



        