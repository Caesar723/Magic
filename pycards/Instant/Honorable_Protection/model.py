
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Honorable_Protection(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Honorable Protection"

        self.type:str="Instant"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Target creature you control gains indestructible until end of turn. If it's a Knight, put a +1/+1 counter on it."
        self.image_path:str="cards/Instant/Honorable Protection/image.jpg"



        