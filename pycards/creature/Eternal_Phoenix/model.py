
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature


class Eternal_Phoenix(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Eternal Phoenix"
        self.live:int=3
        self.power:int=3

        self.type_creature:str="Phoenix Creature - Phoenix"
        self.type:str="Creature"

        self.mana_cost:str="2RR"
        self.color:str="red"
        self.type_card:str="Phoenix Creature - Phoenix"
        self.rarity:str="Rare"
        self.content:str="Flying, When Eternal Phoenix dies, if it didn't have a feather counter on it, return it to the battlefield with a feather counter on it instead of putting it into your graveyard."
        self.image_path:str="cards/creature/Eternal Phoenix/image.jpg"



        