
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Unleash_the_Elements(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Unleash the Elements"

        self.type:str="Sorcery"

        self.mana_cost:str="2RG"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Unleash the Elements deals 3 damage to each creature. If a creature dealt damage this way would die this turn, exile it instead."
        self.image_path:str="cards/sorcery/Unleash the Elements/image.jpg"



        