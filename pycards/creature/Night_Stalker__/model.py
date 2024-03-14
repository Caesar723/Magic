
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature


class Night_Stalker__(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Night Stalker  "
        self.live:int=1
        self.power:int=2

        self.type_creature:str="Vampire Creature  "
        self.type:str="Creature"

        self.mana_cost:str="1B  "
        self.color:str="colorless"
        self.type_card:str="Vampire Creature  "
        self.rarity:str="Common  "
        self.content:str="Menace (This creature can't be blocked except by two or more creatures.)  "
        self.image_path:str="cards/creature/Night Stalker  /image.jpg"



        