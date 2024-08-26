
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Alchemist_s_Chaotic_Blend(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Alchemist's Chaotic Blend"

        self.type:str="Instant"

        self.mana_cost:str="3R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. Then reveal a random card from your library and cast it without paying its mana cost."
        self.image_path:str="cards/Instant/Alchemist's Chaotic Blend/image.jpg"



        