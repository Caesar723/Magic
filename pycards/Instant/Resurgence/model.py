
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Resurgence(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Resurgence"

        self.type:str="Instant"

        self.mana_cost:str="3RW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Creatures you control gain double strike and lifelink until end of turn. Return target creature card with converted mana cost 3 or less from your graveyard to the battlefield."
        self.image_path:str="cards/Instant/Resurgence/image.jpg"



        