
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Vengeful_Retribution(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Vengeful Retribution"

        self.type:str="Instant"

        self.mana_cost:str="4B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Target opponent sacrifices two creatures. If a creature was sacrificed this way, Vengeful Retribution deals damage to any target equal to the total power of the sacrificed creatures."
        self.image_path:str="cards/Instant/Vengeful Retribution/image.jpg"



        