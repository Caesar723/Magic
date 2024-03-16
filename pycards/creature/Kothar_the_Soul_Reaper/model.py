
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Kothar_the_Soul_Reaper(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Kothar the Soul Reaper"
        self.live:int=5
        self.power:int=5
        self.actual_live:int=5
        self.actual_power:int=5

        self.type_creature:str="Demon Creature"
        self.type:str="Creature"

        self.mana_cost:str="4B"
        self.color:str="black"
        self.type_card:str="Demon Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="When Kothar the Soul Reaper enters the battlefield, each opponent sacrifices a creature. Whenever a creature dies, Kothar gets a +1/+1 counter."
        self.image_path:str="cards/creature/Kothar the Soul Reaper/image.jpg"



        