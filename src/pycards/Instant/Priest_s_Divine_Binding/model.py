
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Priest_s_Divine_Binding(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Priest's Divine Binding"

        self.type:str="Instant"

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target creature spell. You gain life equal to that creature's power."
        self.image_path:str="cards/Instant/Priest's Divine Binding/image.jpg"



        