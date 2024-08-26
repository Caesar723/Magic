
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Rogue_s_Trickery(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Rogue's Trickery"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. If the spell is countered this way, exile it. You may cast it this turn by paying its mana cost."
        self.image_path:str="cards/Instant/Rogue's Trickery/image.jpg"



        