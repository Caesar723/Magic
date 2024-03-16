
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Inferno_Titan(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Inferno Titan"
        self.live:int=6
        self.power:int=6
        self.actual_live:int=6
        self.actual_power:int=6

        self.type_creature:str="Elemental Creature"
        self.type:str="Creature"

        self.mana_cost:str="3RR"
        self.color:str="red"
        self.type_card:str="Elemental Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="When Inferno Titan enters the battlefield, it deals 3 damage divided as you choose among one, two, or three target creatures and/or players."
        self.image_path:str="cards/creature/Inferno Titan/image.jpg"



        