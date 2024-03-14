
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.game_function_tool import select_object


class Verdant_Sanctuary(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Verdant Sanctuary"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="green"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Verdant Sanctuary enters the battlefield untapped and adds one green mana to your mana pool. You may also tap Verdant Sanctuary and pay 2 mana to search your library for a basic Forest card and put it onto the battlefield tapped."
        self.image_path:str="cards/land/Verdant Sanctuary/image.jpg"



        