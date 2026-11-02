from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Lastlight_Remedy(Instant):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":1,"life_threshold":8,"heal_low":8,"heal_normal":4}

        self.fixed_id:int=250

        self.name:str="Lastlight Remedy"
        self.type:str="Instant"
        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="If you have {life_threshold} or less life, you gain {heal_low} life and draw {draw_count_article} card{draw_count_plural}. Otherwise, you gain {heal_normal} life."
        self.image_path:str="cards/Instant/Lastlight Remedy/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            if player.life<=self.effect_params["life_threshold"]:
                await self.cure_to_object(player,self.effect_params["heal_low"],"rgba(245, 238, 145, 0.8)","Cure")
                player.draw_card(self.effect_params["draw_count"])
            else:
                await self.cure_to_object(player,self.effect_params["heal_normal"],"rgba(245, 238, 145, 0.8)","Cure")
        finally:
            player.action_store.end_record()
