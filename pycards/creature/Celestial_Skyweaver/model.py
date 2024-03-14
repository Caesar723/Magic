
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Celestial_Skyweaver(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Skyweaver"
        self.live:int=5
        self.power:int=2

        self.type_creature:str="Spirit Creature - Spirit"
        self.type:str="Creature"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Spirit Creature - Spirit"
        self.rarity:str="Rare"
        self.content:str="Flying, Whenever you cast an enchantment spell, you may tap target creature an opponent controls."
        self.image_path:str="cards/creature/Celestial Skyweaver/image.jpg"



        