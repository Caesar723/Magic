
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Spectral_Embrace(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Spectral Embrace"

        self.type:str="Sorcery"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Spectral Embrace gives all creatures you control +2/+2 until end of turn and prevents all damage that would be dealt to them this turn."
        self.image_path:str="cards/sorcery/Spectral Embrace/image.jpg"



        