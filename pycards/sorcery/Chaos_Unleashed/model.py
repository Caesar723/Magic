
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Chaos_Unleashed(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Chaos Unleashed"

        self.type:str="Sorcery"

        self.mana_cost:str="2BR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Chaos Unleashed deals 3 damage to each creature and each player."
        self.image_path:str="cards/sorcery/Chaos Unleashed/image.jpg"



        