
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Flames_of_Fury(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Flames of Fury"

        self.type:str="Sorcery"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Flames of Fury deals 3 damage to target creature or player. If you control a Mountain, Flames of Fury deals 1 additional damage."
        self.image_path:str="cards/sorcery/Flames of Fury/image.jpg"



        