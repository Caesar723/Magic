
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Mystic_Confluence(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Confluence"

        self.type:str="Instant"

        self.mana_cost:str="4U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Choose three. You may choose the same mode more than once. Counter target spell unless its controller pays 3. Return target creature to its owner's hand. Draw a card."
        self.image_path:str="cards/Instant/Mystic Confluence/image.jpg"



        