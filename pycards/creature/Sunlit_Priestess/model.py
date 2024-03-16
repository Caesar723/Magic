
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Sunlit_Priestess(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Sunlit Priestess"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Cleric"
        self.type:str="Creature"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Human Cleric"
        self.rarity:str="Common"
        self.content:str="When Sunlit Priestess enters the battlefield, you gain 3 life."
        self.image_path:str="cards/creature/Sunlit Priestess/image.jpg"



        