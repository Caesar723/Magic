
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Falling_Stars(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Falling Stars"

        self.type:str="Sorcery"

        self.mana_cost:str="7RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Deal 7 damage to all creatures, then summon a 7/7 Star Beast creature token onto the battlefield."
        self.image_path:str="cards/sorcery/Falling Stars/image.jpg"



        