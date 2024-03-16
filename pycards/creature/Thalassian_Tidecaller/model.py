
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Thalassian_Tidecaller(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Thalassian Tidecaller"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Merfolk Creature"
        self.type:str="Creature"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Merfolk Creature"
        self.rarity:str="Rare"
        self.content:str="Whenever you cast a Merfolk spell, you may tap or untap target permanent."
        self.image_path:str="cards/creature/Thalassian Tidecaller/image.jpg"



        