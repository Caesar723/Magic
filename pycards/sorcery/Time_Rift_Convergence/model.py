
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery


class Time_Rift_Convergence(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Time Rift Convergence"

        self.type:str="Sorcery"

        self.mana_cost:str="2UUU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Time Rift Convergence allows you to take an extra turn after this one. Exile Time Rift Convergence."
        self.image_path:str="cards/sorcery/Time Rift Convergence/image.jpg"



        