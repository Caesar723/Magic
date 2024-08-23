
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Verdant_Titan(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Verdant Titan"
        self.live:int=5
        self.power:int=5
        self.actual_live:int=5
        self.actual_power:int=5

        self.type_creature:str="Elemental Creature"
        self.type:str="Creature"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Elemental Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="Trample, Vigilance, When Verdant Titan enters the battlefield or attacks, you may search your library for a land card and put it onto the battlefield tapped. If you do, shuffle your library."
        self.image_path:str="cards/creature/Verdant Titan/image.jpg"



        