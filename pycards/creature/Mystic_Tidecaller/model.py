
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Mystic_Tidecaller(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Tidecaller"
        self.live:int=3
        self.power:int=2

        self.type_creature:str="Merfolk Wizard"
        self.type:str="Creature"

        self.mana_cost:str="3U"
        self.color:str="blue"
        self.type_card:str="Merfolk Wizard"
        self.rarity:str="Mythic Rare"
        self.content:str="Flash, When Mystic Tidecaller enters the battlefield, you may return target nonland permanent to its owner's hand."
        self.image_path:str="cards/creature/Mystic Tidecaller/image.jpg"



        