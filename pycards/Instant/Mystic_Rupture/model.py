
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Mystic_Rupture(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Rupture"

        self.type:str="Instant"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Return all nonland permanents to their owner's hands. Each player may search their library for a basic land card, put it onto the battlefield tapped, then shuffle their library."
        self.image_path:str="cards/Instant/Mystic Rupture/image.jpg"



        