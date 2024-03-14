
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Torrential_Manipulation(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Torrential Manipulation"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Return target nonland permanent to its owner's hand. You may cast an instant or sorcery spell without paying its mana cost."
        self.image_path:str="cards/sorcery/Torrential Manipulation/image.jpg"



        