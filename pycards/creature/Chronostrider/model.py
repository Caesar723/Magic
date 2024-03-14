
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature


class Chronostrider(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Chronostrider"
        self.live:int=4
        self.power:int=2

        self.type_creature:str="Human Wizard"
        self.type:str="Creature"

        self.mana_cost:str="3G"
        self.color:str="green"
        self.type_card:str="Human Wizard"
        self.rarity:str="Mythic Rare"
        self.content:str="Flash, Haste. When Chronostrider enters the battlefield, you may take an extra turn after this one."
        self.image_path:str="cards/creature/Chronostrider/image.jpg"



        