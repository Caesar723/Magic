
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Soul_Transfer(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Soul Transfer"

        self.type:str="Sorcery"

        self.mana_cost:str="4BB"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Choose one creature. That creature gains all abilities of a creature card in any graveyard of your choice."
        self.image_path:str="cards/sorcery/Soul Transfer/image.jpg"



        