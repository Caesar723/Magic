
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Witch_s_Curse_Counter(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Witch's Curse Counter"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. Then, its controller gains a curse for three turns, reducing their strength and stamina by half."
        self.image_path:str="cards/Instant/Witch's Curse Counter/image.jpg"



        