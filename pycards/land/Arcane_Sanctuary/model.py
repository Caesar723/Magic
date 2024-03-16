
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.game_function_tool import select_object


class Arcane_Sanctuary(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Arcane Sanctuary"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="black"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Arcane Sanctuary enters the battlefield untapped and adds one colorless mana to your mana pool. You may also tap Arcane Sanctuary and pay 2 mana to scry 1 and draw a card."
        self.image_path:str="cards/land/Arcane Sanctuary/image.jpg"



        