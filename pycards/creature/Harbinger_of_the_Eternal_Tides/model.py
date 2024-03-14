
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Harbinger_of_the_Eternal_Tides(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Harbinger of the Eternal Tides"
        self.live:int=4
        self.power:int=2

        self.type_creature:str="Merfolk Creature - Merfolk"
        self.type:str="Creature"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Merfolk Creature - Merfolk"
        self.rarity:str="Rare"
        self.content:str="Flash, When Harbinger of the Eternal Tides enters the battlefield, tap target creature an opponent controls. It doesn't untap during its controller's next untap step."
        self.image_path:str="cards/creature/Harbinger of the Eternal Tides/image.jpg"



        