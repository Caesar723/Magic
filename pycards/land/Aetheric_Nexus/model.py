
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.game_function_tool import select_object


class Aetheric_Nexus(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Aetheric Nexus"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="gold"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Aetheric Nexus enters the battlefield untapped and adds one colorless mana to your mana pool. You may also tap Aetheric Nexus to add one mana of any color, but only if you control an artifact."
        self.image_path:str="cards/land/Aetheric Nexus/image.jpg"



        