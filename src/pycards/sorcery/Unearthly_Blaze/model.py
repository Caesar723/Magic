
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Unearthly_Blaze(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Unearthly Blaze"

        self.type:str="Sorcery"

        self.mana_cost:str="1RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Unearthly Blaze deals 3 damage to any target."
        self.image_path:str="cards/sorcery/Unearthly Blaze/image.jpg"



        