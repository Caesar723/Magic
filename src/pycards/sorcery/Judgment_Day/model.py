
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Judgment_Day(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Judgment Day"

        self.type:str="Sorcery"

        self.mana_cost:str="5WW"
        self.color:str="colorless"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Destroy all creatures. Then, each player may return one creature card from their graveyard to the battlefield."
        self.image_path:str="cards/sorcery/Judgment Day/image.jpg"



        