
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Necromancer_s_Soul_Seize(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Necromancer's Soul Seize"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target creature spell. If the spell is countered this way, exile a card from your library, then return a card of the same type from your graveyard to your hand."
        self.image_path:str="cards/Instant/Necromancer's Soul Seize/image.jpg"



        