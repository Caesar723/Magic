
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Shifting_Tides_Elemental(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Shifting Tides Elemental"
        self.live:int=3
        self.power:int=2
        self.actual_live:int=3
        self.actual_power:int=2

        self.type_creature:str="Elemental Creature - Elemental"
        self.type:str="Creature"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Elemental Creature - Elemental"
        self.rarity:str="Uncommon"
        self.content:str="Islandwalk (This creature can't be blocked as long as defending player controls an Island.), When Shifting Tides Elemental enters the battlefield, you may return target land to its owner's hand."
        self.image_path:str="cards/creature/Shifting Tides Elemental/image.jpg"



        