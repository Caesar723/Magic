
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature


class Thunderclap_Behemoth(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Thunderclap Behemoth"
        self.live:int=6
        self.power:int=6

        self.type_creature:str="Beast Creature - Beast"
        self.type:str="Creature"

        self.mana_cost:str="4GG"
        self.color:str="green"
        self.type_card:str="Beast Creature - Beast"
        self.rarity:str="Rare"
        self.content:str="Trample (This creature can deal excess combat damage to the player or planeswalker it's attacking.), Whenever Thunderclap Behemoth attacks, it deals 3 damage to each creature defending player controls if you control another creature with power 4 or greater."
        self.image_path:str="cards/creature/Thunderclap Behemoth/image.jpg"



        