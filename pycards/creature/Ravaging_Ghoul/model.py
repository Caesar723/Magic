
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Ravaging_Ghoul(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Ravaging Ghoul"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Zombie Creature"
        self.type:str="Creature"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Zombie Creature"
        self.rarity:str="Uncommon"
        self.content:str="When Ravaging Ghoul enters the battlefield, target opponent loses 2 life unless they sacrifice a creature."
        self.image_path:str="cards/creature/Ravaging Ghoul/image.jpg"



        