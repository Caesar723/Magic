
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Mystical_Barrier(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystical Barrier"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target spell unless its controller pays 3. If Mystical Barrier is countered this way, you may draw a card."
        self.image_path:str="cards/Instant/Mystical Barrier/image.jpg"



        