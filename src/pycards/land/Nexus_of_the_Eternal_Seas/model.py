
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.game_function_tool import select_object


class Nexus_of_the_Eternal_Seas(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Nexus of the Eternal Seas"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="blue"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Nexus of the Eternal Seas enters the battlefield untapped and adds one blue mana to your mana pool. You may tap Nexus of the Eternal Seas to return target creature to its owner's hand."
        self.image_path:str="cards/land/Nexus of the Eternal Seas/image.jpg"



        