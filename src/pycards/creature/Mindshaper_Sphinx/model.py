
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Mindshaper_Sphinx(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mindshaper Sphinx"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Sphinx Creature - Sphinx"
        self.type:str="Creature"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Sphinx Creature - Sphinx"
        self.rarity:str="Rare"
        self.content:str="Flying, When Mindshaper Sphinx enters the battlefield, scry 3, then draw a card. (To scry 3, look at the top three cards of your library, then put any number of them on the bottom of your library and the rest on top in any order.)"
        self.image_path:str="cards/creature/Mindshaper Sphinx/image.jpg"



        