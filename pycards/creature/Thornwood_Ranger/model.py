
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature


class Thornwood_Ranger(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Thornwood Ranger"
        self.live:int=1
        self.power:int=2

        self.type_creature:str="Human Warrior"
        self.type:str="Creature"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Human Warrior"
        self.rarity:str="Common"
        self.content:str="Reach (This creature can block creatures with flying.)"
        self.image_path:str="cards/creature/Thornwood Ranger/image.jpg"



        