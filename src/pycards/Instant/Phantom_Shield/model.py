
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Phantom_Shield(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Phantom Shield"

        self.type:str="Instant"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until end of turn, your creatures gain 'Prevent all damage that would be dealt to this creature this turn.'"
        self.image_path:str="cards/Instant/Phantom Shield/image.jpg"



        