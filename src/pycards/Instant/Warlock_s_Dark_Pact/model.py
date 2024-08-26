
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Warlock_s_Dark_Pact(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Warlock's Dark Pact"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. Its controller loses life equal to its mana cost."
        self.image_path:str="cards/Instant/Warlock's Dark Pact/image.jpg"



        