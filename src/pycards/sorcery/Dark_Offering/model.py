
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Dark_Offering(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Dark Offering"

        self.type:str="Sorcery"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Target player loses 2 life and you gain 2 life."
        self.image_path:str="cards/sorcery/Dark Offering/image.jpg"



        