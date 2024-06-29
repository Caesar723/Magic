
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Temporal_Distortion(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Temporal Distortion"

        self.type:str="Sorcery"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Temporal Distortion allows you to take an extra turn after this one. Exile Temporal Distortion."
        self.image_path:str="cards/sorcery/Temporal Distortion/image.jpg"



        