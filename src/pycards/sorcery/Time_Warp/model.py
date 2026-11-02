
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random

class Time_Warp(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":2,"discard_count":1}

        self.name:str="Time Warp"

        self.type:str="Sorcery"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Draw {draw_count_word} card{draw_count_plural}, then randomly discard {discard_count_article} card{discard_count_plural}. You may put a card from your graveyard on top of your library."
        self.image_path:str="cards/sorcery/Time Warp/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        player.draw_card(self.effect_params["draw_count"])
        for _ in range(self.effect_params["discard_count"]):
            if player.hand:
                card=random.choice(player.hand)
                player.discard(card)
        cards=random.sample(player.graveyard,1)
        if cards:
            card=cards[0]
            player.remove_card(card,"graveyard")
            player.library.insert(0,card.copy_for_player(player))


        