
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Veil_of_Serenity(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Veil of Serenity"

        self.type:str="Instant"

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Exile target enchantment or creature spell."
        self.image_path:str="cards/Instant/Veil of Serenity/image.jpg"



        