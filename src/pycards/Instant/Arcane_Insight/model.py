
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
import random


class Arcane_Insight(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":2}

        self.name:str="Arcane Insight"

        self.type:str="Instant"

        self.mana_cost:str="2U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Draw {draw_count_word} card{draw_count_plural}, then randomly discard a card unless you discard an instant or sorcery card."
        self.image_path:str="cards/Instant/Arcane Insight/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        player.draw_card(self.effect_params["draw_count"])
        if not player.hand:
            return
        card=random.choice(player.hand)
        if card.type not in ("Instant","Sorcery"):
            return
        player.discard(card)

