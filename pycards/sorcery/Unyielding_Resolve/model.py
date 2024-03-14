
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery


class Unyielding_Resolve(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Unyielding Resolve"

        self.type:str="Sorcery"

        self.mana_cost:str="3WW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Unyielding Resolve gives all creatures you control indestructible until end of turn. Creatures you control gain lifelink until end of turn."
        self.image_path:str="cards/sorcery/Unyielding Resolve/image.jpg"



        