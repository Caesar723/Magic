
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land


class Sanctum_of_Verdant_Growth(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Sanctum of Verdant Growth"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="green"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Sanctum of Verdant Growth enters the battlefield untapped and adds one green mana to your mana pool. You may tap Sanctum of Verdant Growth and pay 2 mana to search your library for a basic Forest card and put it onto the battlefield tapped."
        self.image_path:str="cards/land/Sanctum of Verdant Growth/image.jpg"



        