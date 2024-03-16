
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Dreamweaver_Archivist(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Dreamweaver Archivist"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Wizard"
        self.type:str="Creature"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Human Wizard"
        self.rarity:str="Rare"
        self.content:str="When Dreamweaver Archivist enters the battlefield, you may draw a card. If you do, discard a card."
        self.image_path:str="cards/creature/Dreamweaver Archivist/image.jpg"



        