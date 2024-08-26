
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Titan_Giant(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Titan Giant"
        self.live:int=8
        self.power:int=8
        self.actual_live:int=8
        self.actual_power:int=8

        self.type_creature:str="Creature - Giant"
        self.type:str="Creature"

        self.mana_cost:str="5GG"
        self.color:str="green"
        self.type_card:str="Creature - Giant"
        self.rarity:str="Rare"
        self.content:str="Whenever Titan Giant enters the battlefield, destroy all other creatures with power less than 5."
        self.image_path:str="cards/creature/Titan Giant/image.jpg"



        