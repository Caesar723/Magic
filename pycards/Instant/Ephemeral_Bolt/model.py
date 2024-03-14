
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Ephemeral_Bolt(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Ephemeral Bolt"

        self.type:str="Instant"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Ephemeral Bolt deals 3 damage to target creature or player. If Ephemeral Bolt is in your graveyard, you may cast it for its flashback cost. If you do, exile it as it resolves."
        self.image_path:str="cards/Instant/Ephemeral Bolt/image.jpg"



        