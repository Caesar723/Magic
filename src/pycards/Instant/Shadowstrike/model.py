
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Shadowstrike(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Shadowstrike"

        self.type:str="Instant"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Destroy target tapped creature. If a creature was destroyed this way, you may draw a card."
        self.image_path:str="cards/Instant/Shadowstrike/image.jpg"



        