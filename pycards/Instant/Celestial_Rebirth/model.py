
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Celestial_Rebirth(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Celestial Rebirth"

        self.type:str="Instant"

        self.mana_cost:str="2WWW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Return target creature card from your graveyard to the battlefield. It gains indestructible until end of turn. Exile Celestial Rebirth."
        self.image_path:str="cards/Instant/Celestial Rebirth/image.jpg"



        