
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Summoner_s_Arcane_Acquisition(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Summoner's Arcane Acquisition"

        self.type:str="Instant"

        self.mana_cost:str="2G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. If the spell is countered this way, create an Elemental creature token with power and toughness equal to that spell's mana cost."
        self.image_path:str="cards/Instant/Summoner's Arcane Acquisition/image.jpg"



        