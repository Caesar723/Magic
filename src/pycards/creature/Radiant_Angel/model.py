
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Radiant_Angel(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Radiant Angel"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Creature - Angel"
        self.type:str="Creature"

        self.mana_cost:str="3WW"
        self.color:str="gold"
        self.type_card:str="Creature - Angel"
        self.rarity:str="Rare"
        self.content:str="Flying, Lifelink. Whenever Radiant Angel deals damage, it illuminates all creatures with dark attributes, making them unable to attack or block this turn."
        self.image_path:str="cards/creature/Radiant Angel/image.jpg"



        