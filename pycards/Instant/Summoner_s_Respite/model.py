
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Summoner_s_Respite(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Summoner's Respite"

        self.type:str="Instant"

        self.mana_cost:str="3GW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Prevent all combat damage that would be dealt this turn. You gain 4 life. Put a +1/+1 counter on each creature you control."
        self.image_path:str="cards/Instant/Summoner's Respite/image.jpg"



        