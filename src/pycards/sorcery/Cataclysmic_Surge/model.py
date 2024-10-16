
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Cataclysmic_Surge(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Cataclysmic Surge"

        self.type:str="Sorcery"

        self.mana_cost:str="3RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Cataclysmic Surge deals 5 damage to each creature and each player. If a creature dealt damage this way would die this turn, exile it instead."
        self.image_path:str="cards/sorcery/Cataclysmic Surge/image.jpg"



        