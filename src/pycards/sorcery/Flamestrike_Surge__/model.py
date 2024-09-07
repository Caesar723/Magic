
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Flamestrike_Surge__(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Flamestrike Surge"

        self.type:str="Sorcery"

        self.mana_cost:str="1RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Flamestrike Surge deals 3 damage to any target and you may discard a card. If you do, draw a card."
        self.image_path:str="cards/sorcery/Flamestrike Surge/image.jpg"



        