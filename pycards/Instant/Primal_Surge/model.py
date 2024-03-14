
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Primal_Surge(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Primal Surge"

        self.type:str="Instant"

        self.mana_cost:str="2G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Target player shuffles their hand and graveyard into their library, then draws that many cards. They may play an additional land this turn."
        self.image_path:str="cards/Instant/Primal Surge/image.jpg"



        