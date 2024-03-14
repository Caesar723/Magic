
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery


class Eldritch_Rebirth(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Eldritch Rebirth"

        self.type:str="Sorcery"

        self.mana_cost:str="2GG"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Eldritch Rebirth allows you to return all creature cards with converted mana cost 3 or less from your graveyard to the battlefield. If Eldritch Rebirth was cast from your graveyard, you may return all creature cards with converted mana cost 4 or greater from your graveyard to the battlefield instead."
        self.image_path:str="cards/sorcery/Eldritch Rebirth/image.jpg"



        