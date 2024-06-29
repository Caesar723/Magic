
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Astral_Resurgence(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Astral Resurgence"

        self.type:str="Instant"

        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Return all creature cards from your graveyard to the battlefield. They gain lifelink until end of turn."
        self.image_path:str="cards/Instant/Astral Resurgence/image.jpg"



        