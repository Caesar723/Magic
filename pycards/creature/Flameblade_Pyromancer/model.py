
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Flameblade_Pyromancer(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Flameblade Pyromancer"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Shaman"
        self.type:str="Creature"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Human Shaman"
        self.rarity:str="Uncommon"
        self.content:str="When Flameblade Pyromancer enters the battlefield, you may discard a card. If you do, it deals 2 damage to target creature or player."
        self.image_path:str="cards/creature/Flameblade Pyromancer/image.jpg"



        