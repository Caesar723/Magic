
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Seraph_of_the_Eternal_Flame(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Seraph of the Eternal Flame"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Angel"
        self.type:str="Creature"

        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Angel"
        self.rarity:str="Rare"
        self.content:str="Radiant Aura - Whenever Seraph of the Eternal Flame attacks, creatures you control gain indestructible until end of turn."
        self.image_path:str="cards/creature/Seraph of the Eternal Flame/image.jpg"



        