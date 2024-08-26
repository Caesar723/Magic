
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Ranger_s_Sniping_Shot(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ranger's Sniping Shot"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. If that spell is a creature spell, deal damage to its controller equal to that creature's power."
        self.image_path:str="cards/Instant/Ranger's Sniping Shot/image.jpg"



        