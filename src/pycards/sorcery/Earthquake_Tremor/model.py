
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Earthquake_Tremor(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Earthquake Tremor"

        self.type:str="Sorcery"

        self.mana_cost:str="6RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Destroy all non-creature permanents. For each permanent destroyed this way, create a 3/3 Elemental creature token."
        self.image_path:str="cards/sorcery/Earthquake Tremor/image.jpg"



        