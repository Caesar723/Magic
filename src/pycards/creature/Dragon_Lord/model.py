
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Dragon_Lord(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Dragon Lord"
        self.live:int=6
        self.power:int=6
        self.actual_live:int=6
        self.actual_power:int=6

        self.type_creature:str="Creature - Dragon"
        self.type:str="Creature"

        self.mana_cost:str="6RR"
        self.color:str="red"
        self.type_card:str="Creature - Dragon"
        self.rarity:str="Rare"
        self.content:str="Flying. Whenever Dragon Lord deals damage to an opponent, create two 4/4 red Dragon creature tokens."
        self.image_path:str="cards/creature/Dragon Lord/image.jpg"



        