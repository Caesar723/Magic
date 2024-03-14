
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery


class Divine_Rebirth(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Divine Rebirth"

        self.type:str="Sorcery"

        self.mana_cost:str="3W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Return target creature card from your graveyard to the battlefield. If it's an Angel, create two 4/4 white Angel creature tokens with flying tapped and attacking."
        self.image_path:str="cards/sorcery/Divine Rebirth/image.jpg"



        