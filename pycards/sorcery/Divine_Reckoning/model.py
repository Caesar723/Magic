
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Divine_Reckoning(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Divine Reckoning"

        self.type:str="Sorcery"

        self.mana_cost:str="4W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Destroy all non-angel creatures. Each player gains life equal to the number of creatures they controlled that were destroyed this way."
        self.image_path:str="cards/sorcery/Divine Reckoning/image.jpg"



        