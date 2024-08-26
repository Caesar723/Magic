
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Shadow_Stalker(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Shadow Stalker"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Creature - Assassin"
        self.type:str="Creature"

        self.mana_cost:str="3BB"
        self.color:str="black"
        self.type_card:str="Creature - Assassin"
        self.rarity:str="Rare"
        self.content:str="Cannot be targeted by spells or abilities. Whenever Shadow Stalker attacks, the controller of the target creature discards a card."
        self.image_path:str="cards/creature/Shadow Stalker/image.jpg"



        