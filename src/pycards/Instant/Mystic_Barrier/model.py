
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Mystic_Barrier(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystic Barrier"

        self.type:str="Instant"

        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Choose one - Target creature gains hexproof until end of turn.Target player can't cast noncreature spells until end of turn."
        self.image_path:str="cards/Instant/Mystic Barrier/image.jpg"



        