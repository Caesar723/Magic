
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Mind_s_Insight(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mind's Insight"

        self.type:str="Sorcery"

        self.mana_cost:str="4U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Draw three cards, then discard two cards unless you discard an island."
        self.image_path:str="cards/sorcery/Mind's Insight/image.jpg"



        