
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Ephemeral_Insight(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ephemeral Insight"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Scry 2, then draw a card. If Ephemeral Insight is in your graveyard, you may cast it by paying 3 life in addition to its mana cost. If you do, exile it as it resolves."
        self.image_path:str="cards/Instant/Ephemeral Insight/image.jpg"



        