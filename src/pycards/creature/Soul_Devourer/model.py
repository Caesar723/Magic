
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Soul_Devourer(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Soul Devourer"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Creature - Demon"
        self.type:str="Creature"

        self.mana_cost:str="4BB"
        self.color:str="black"
        self.type_card:str="Creature - Demon"
        self.rarity:str="Rare"
        self.content:str="Whenever a creature dies, Soul Devourer gets +1/+1 counters equal to the power of that creature."
        self.image_path:str="cards/creature/Soul Devourer/image.jpg"



        