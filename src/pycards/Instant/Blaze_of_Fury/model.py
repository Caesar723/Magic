
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Blaze_of_Fury(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Blaze of Fury"

        self.type:str="Instant"

        self.mana_cost:str="1RR"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Blaze of Fury deals 3 damage to any target. If a creature is dealt damage this way, it can't block this turn."
        self.image_path:str="cards/Instant/Blaze of Fury/image.jpg"



        