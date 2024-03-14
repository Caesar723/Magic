
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Mindful_Reflection(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mindful Reflection"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Draw two cards, then discard a card."
        self.image_path:str="cards/sorcery/Mindful Reflection/image.jpg"



        