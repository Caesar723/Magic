
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Overgrowth_Surge(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Overgrowth Surge"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Target creature gets +3/+3 until end of turn. If that creature is a Treefolk, it also gains trample until end of turn."
        self.image_path:str="cards/Instant/Overgrowth Surge/image.jpg"



        