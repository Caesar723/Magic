
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Rift_in_Reality(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Rift in Reality"

        self.type:str="Sorcery"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Rift in Reality allows you to exile target permanent. At the beginning of the next end step, return the exiled card to the battlefield under its owner's control with a sleight of hand counter on it. If it doesn't have sleight of hand counter on it, it's owner draws a card."
        self.image_path:str="cards/sorcery/Rift in Reality/image.jpg"



        