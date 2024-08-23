
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Grove_Guardian(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Grove Guardian"
        self.live:int=5
        self.power:int=3
        self.actual_live:int=5
        self.actual_power:int=3

        self.type_creature:str="Elemental Creature - Elemental"
        self.type:str="Creature"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Elemental Creature - Elemental"
        self.rarity:str="Uncommon"
        self.content:str="Reach, Hexproof (This creature can't be the target of spells or abilities your opponents control.)"
        self.image_path:str="cards/creature/Grove Guardian/image.jpg"



        