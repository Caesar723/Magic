
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Ancient_Stonewood(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ancient Stonewood"
        self.live:int=7
        self.power:int=5
        self.actual_live:int=7
        self.actual_power:int=5

        self.type_creature:str="Creature - Treefolk"
        self.type:str="Creature"

        self.mana_cost:str="4GG"
        self.color:str="green"
        self.type_card:str="Creature - Treefolk"
        self.rarity:str="Rare"
        self.content:str="Indestructible. Whenever Ancient Stonewood is dealt damage, it deals that much damage to target creature an opponent controls."
        self.image_path:str="cards/creature/Ancient Stonewood/image.jpg"



        