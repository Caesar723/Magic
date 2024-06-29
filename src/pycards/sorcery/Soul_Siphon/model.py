
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Soul_Siphon(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Soul Siphon"

        self.type:str="Sorcery"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Target opponent sacrifices a creature. You gain life equal to that creature's power."
        self.image_path:str="cards/sorcery/Soul Siphon/image.jpg"



        