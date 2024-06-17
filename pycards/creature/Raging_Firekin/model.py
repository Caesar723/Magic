
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Raging_Firekin(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Raging Firekin"
        self.live:int=2
        self.power:int=3
        self.actual_live:int=2
        self.actual_power:int=3

        self.type_creature:str="Elemental Creature - Elemental"
        self.type:str="Creature"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Elemental Creature - Elemental"
        self.rarity:str="Uncommon"
        self.content:str="Trample (This creature can deal excess combat damage to the player or planeswalker it's attacking.)"
        self.image_path:str="cards/creature/Raging Firekin/image.jpg"

        self.flag_dict["Trample"]=True



        