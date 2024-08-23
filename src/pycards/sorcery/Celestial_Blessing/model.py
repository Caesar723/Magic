
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Celestial_Blessing(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Celestial Blessing"

        self.type:str="Sorcery"

        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Choose up to two target creatures you control. They gain lifelink until end of turn."
        self.image_path:str="cards/sorcery/Celestial Blessing/image.jpg"



        