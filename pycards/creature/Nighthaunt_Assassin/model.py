
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Nighthaunt_Assassin(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Nighthaunt Assassin"
        self.live:int=1
        self.power:int=2
        self.actual_live:int=1
        self.actual_power:int=2

        self.type_creature:str="Human Rogue"
        self.type:str="Creature"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Human Rogue"
        self.rarity:str="Rare"
        self.content:str="When Nighthaunt Assassin enters the battlefield, you may destroy target creature with converted mana cost 2 or less."
        self.image_path:str="cards/creature/Nighthaunt Assassin/image.jpg"



        