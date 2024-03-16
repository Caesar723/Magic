
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Thornwood_Guardian(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Thornwood Guardian"
        self.live:int=4
        self.power:int=5
        self.actual_live:int=4
        self.actual_power:int=5

        self.type_creature:str="Elemental Creature - Elemental"
        self.type:str="Creature"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Elemental Creature - Elemental"
        self.rarity:str="Rare"
        self.content:str="Reach, Trample (This creature can block creatures with flying, and it can deal excess combat damage to the player or planeswalker it's attacking.)"
        self.image_path:str="cards/creature/Thornwood Guardian/image.jpg"



        