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

        self.fixed_id:int=250

        self.name:str="Lastlight Remedy"
        self.type:str="Instant"
        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="If you have 8 or less life, you gain 8 life and draw a card. Otherwise, you gain 4 life."
        self.image_path:str="cards/Instant/Lastlight Remedy/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            if player.life<=8:
                await self.cure_to_object(player,8,"rgba(245, 238, 145, 0.8)","Cure")
                player.draw_card(1)
            else:
                await self.cure_to_object(player,4,"rgba(245, 238, 145, 0.8)","Cure")
        finally:
            player.action_store.end_record()
