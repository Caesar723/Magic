
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Shadowform_Surge(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Shadowform Surge"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Target creature gets -3/-3 until end of turn. If that creature dies this turn, create a 2/2 black Shade creature token with lifelink."
        self.image_path:str="cards/Instant/Shadowform Surge/image.jpg"



        