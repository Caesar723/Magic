
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Vampiric_Revelry(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Vampiric Revelry"

        self.type:str="Sorcery"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Target player sacrifices a creature. You gain life equal to that creature's toughness."
        self.image_path:str="cards/sorcery/Vampiric Revelry/image.jpg"



        