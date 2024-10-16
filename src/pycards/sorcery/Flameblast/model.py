
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Flameblast(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Flameblast"

        self.type:str="Sorcery"

        self.mana_cost:str="3RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Flameblast deals 5 damage to any target. If RRR was spent to cast Flameblast, it deals 7 damage instead."
        self.image_path:str="cards/sorcery/Flameblast/image.jpg"



        