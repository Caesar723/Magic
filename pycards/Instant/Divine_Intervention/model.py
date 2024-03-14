
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Divine_Intervention(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Divine Intervention"

        self.type:str="Instant"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Choose up to two target creatures. Prevent all damage that would be dealt to those creatures this turn. Gain life equal to the total damage prevented this way."
        self.image_path:str="cards/Instant/Divine Intervention/image.jpg"



        