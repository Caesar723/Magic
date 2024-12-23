
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 

from game.type_cards.creature import Creature
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Angelic_Blessing(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Angelic Blessing"

        self.type:str="Sorcery"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Target creature gets +3/+3 and gains vigilance until end of turn."
        self.image_path:str="cards/sorcery/Angelic Blessing/image.jpg"

    
        