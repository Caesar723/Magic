
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Time_Warp(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"extra_turns":1}

        self.name:str="Time Warp"

        self.type:str="Instant"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Time Warp allows you to take {extra_turns_article_an} extra turn{extra_turns_plural} after this one. You skip the untap step of that turn."
        self.image_path:str="cards/Instant/Time Warp/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        player.add_counter_dict("extra_turn",self.effect_params["extra_turns"])


        