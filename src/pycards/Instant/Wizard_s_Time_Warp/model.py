
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object


class Wizard_s_Time_Warp(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"discard_count":1}

        self.fixed_id:int=88

        self.name:str="Wizard's Time Warp"

        self.type:str="Instant"

        self.mana_cost:str="3U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Counter target spell. Its controller discards {discard_count_article} card{discard_count_plural}."
        self.image_path:str="cards/Instant/Wizard's Time Warp/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        func,card=await self.undo_stack(player,opponent)
        for _ in range(self.effect_params["discard_count"]):
            if opponent.hand:
                card=random.choice(opponent.hand)
                opponent.discard(card)
       


        