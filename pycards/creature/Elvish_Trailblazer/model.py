
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Elvish_Trailblazer(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Elvish Trailblazer"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Elf Creature"
        self.type:str="Creature"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Elf Creature"
        self.rarity:str="Uncommon"
        self.content:str="Reach. When Elvish Trailblazer enters the battlefield, you may search your library for a basic land card, reveal it, and put it into your hand. If you do, shuffle your library."
        self.image_path:str="cards/creature/Elvish Trailblazer/image.jpg"



        