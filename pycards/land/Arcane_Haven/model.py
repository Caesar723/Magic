
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.game_function_tool import select_object


class Arcane_Haven(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Arcane Haven"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="colorless"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Arcane Haven enters the battlefield untapped and adds one colorless mana to your mana pool. You may also tap Arcane Haven to add one mana of any color to your mana pool if you control a wizard."
        self.image_path:str="cards/land/Arcane Haven/image.jpg"



        