
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Storm_Bringer(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Storm Bringer"
        self.live:int=5
        self.power:int=5
        self.actual_live:int=5
        self.actual_power:int=5

        self.type_creature:str="Creature - Elemental"
        self.type:str="Creature"

        self.mana_cost:str="4UU (6 Mana)"
        self.color:str="colorless"
        self.type_card:str="Creature - Elemental"
        self.rarity:str="Rare"
        self.content:str="Flying. When Storm Bringer enters the battlefield, it deals 3 damage to each opponent and you gain 3 life."
        self.image_path:str="cards/creature/Storm Bringer/image.jpg"



        