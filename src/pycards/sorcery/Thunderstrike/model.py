
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Thunderstrike(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Thunderstrike"

        self.type:str="Sorcery"

        self.mana_cost:str="3RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Choose one creature. Thunderstrike deals 8 damage to that creature. If that creature dies, Thunderstrike deals the same amount of damage to each opponent."
        self.image_path:str="cards/sorcery/Thunderstrike/image.jpg"



        