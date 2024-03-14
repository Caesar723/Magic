
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Mystic_Tide(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Tide"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell unless its controller pays 3. If you control an Island, you may return target creature to its owner's hand."
        self.image_path:str="cards/Instant/Mystic Tide/image.jpg"



        