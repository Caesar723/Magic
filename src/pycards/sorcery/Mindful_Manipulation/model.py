
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random


class Mindful_Manipulation(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":2}

        self.name:str="Mindful Manipulation"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Draw {draw_count_word} card{draw_count_plural}, then put one random card from your hand on top of your library."
        self.image_path:str="cards/sorcery/Mindful Manipulation/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        player.draw_card(self.effect_params["draw_count"])
        if not player.hand:
            return
        card=random.choice(player.hand)
        player.remove_card(card,"hand")
        player.library.insert(0,card)

