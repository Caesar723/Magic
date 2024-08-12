
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Luminous_Guardian(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Luminous Guardian"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Angel Creature - Angel"
        self.type:str="Creature"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Angel Creature - Angel"
        self.rarity:str="Rare"
        self.content:str="Flying, Lifelink (Damage dealt by this creature also causes you to gain that much life), When Luminous Guardian enters the battlefield, you may exile target creature with power 3 or greater an opponent controls until Luminous Guardian leaves the battlefield."
        self.image_path:str="cards/creature/Luminous Guardian/image.jpg"


        self.flag_dict['lifelink']=True
        self.flag_dict['flying']=True
        