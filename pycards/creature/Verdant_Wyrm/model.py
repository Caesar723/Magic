
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Verdant_Wyrm(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Verdant Wyrm"
        self.live:int=4
        self.power:int=4

        self.type_creature:str="Dragon Creature - Dragon"
        self.type:str="Creature"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Dragon Creature - Dragon"
        self.rarity:str="Rare"
        self.content:str="Trample, When Verdant Wyrm enters the battlefield, you may search your library for a land card, put it onto the battlefield tapped, then shuffle your library."
        self.image_path:str="cards/creature/Verdant Wyrm/image.jpg"



        