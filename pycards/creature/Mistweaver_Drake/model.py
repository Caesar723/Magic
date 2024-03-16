
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Mistweaver_Drake(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mistweaver Drake"
        self.live:int=1
        self.power:int=2
        self.actual_live:int=1
        self.actual_power:int=2

        self.type_creature:str="Creature - Elemental"
        self.type:str="Creature"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Creature - Elemental"
        self.rarity:str="Common"
        self.content:str="Flash (You may cast this spell any time you could cast an instant)"
        self.image_path:str="cards/creature/Mistweaver Drake/image.jpg"



        