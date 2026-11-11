
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random


class Mind_s_Insight(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":3}

        self.name:str="Mind's Insight"

        self.type:str="Sorcery"

        self.mana_cost:str="4U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Draw {draw_count_word} card{draw_count_plural}, then randomly discard one card unless you discard an island."
        self.image_path:str="cards/sorcery/Mind's Insight/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        player.draw_card(self.effect_params["draw_count"])
        if not player.hand:
            return
        discard_candidates=random.choice(player.hand)
        if discard_candidates.type_card not in ("Island"):
            player.discard(discard_candidates)
        
