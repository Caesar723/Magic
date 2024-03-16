
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Angelic_Protector(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Angelic Protector"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Angel Creature"
        self.type:str="Creature"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Angel Creature"
        self.rarity:str="Uncommon"
        self.content:str="When Angelic Protector enters the battlefield, you may tap target creature. It doesn't untap during its controller's next untap step."
        self.image_path:str="cards/creature/Angelic Protector/image.jpg"



        