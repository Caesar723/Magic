
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Wild_Growth_Rush(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Wild Growth Rush"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Target creature gains +2/+2 and trample until end of turn. Then, if you control a Forest, you may search your library for a basic land card and put it onto the battlefield tapped."
        self.image_path:str="cards/Instant/Wild Growth Rush/image.jpg"



        