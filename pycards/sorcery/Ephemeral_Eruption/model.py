
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Ephemeral_Eruption(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Ephemeral Eruption"

        self.type:str="Sorcery"

        self.mana_cost:str="2RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Ephemeral Eruption deals 4 damage to each creature. At the beginning of the next end step, sacrifice Ephemeral Eruption and return all creatures dealt damage this way to the battlefield under their owner's control."
        self.image_path:str="cards/sorcery/Ephemeral Eruption/image.jpg"



        