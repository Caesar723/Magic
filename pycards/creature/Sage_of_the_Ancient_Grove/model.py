
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Sage_of_the_Ancient_Grove(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Sage of the Ancient Grove"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Treefolk Creature - Treefolk"
        self.type:str="Creature"

        self.mana_cost:str="2GG"
        self.color:str="green"
        self.type_card:str="Treefolk Creature - Treefolk"
        self.rarity:str="Rare"
        self.content:str="Reach, When Sage of the Ancient Grove enters the battlefield, you may search your library for a basic land card, put it onto the battlefield tapped, then shuffle your library."
        self.image_path:str="cards/creature/Sage of the Ancient Grove/image.jpg"



        