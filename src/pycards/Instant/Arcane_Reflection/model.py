
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Arcane_Reflection(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Arcane Reflection"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Arcane Reflection allows you to return target instant or sorcery card from your graveyard to your hand."
        self.image_path:str="cards/Instant/Arcane Reflection/image.jpg"



        