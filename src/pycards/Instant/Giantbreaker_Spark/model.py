from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Giantbreaker_Spark(Instant):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=249

        self.name:str="Giantbreaker Spark"
        self.type:str="Instant"
        self.mana_cost:str="1RR"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Giantbreaker Spark deals 6 damage to target creature an opponent controls if its power is 4 or greater. Otherwise, it deals 3 damage to that creature."
        self.image_path:str="cards/Instant/Giantbreaker Spark/image.jpg"

    @select_object("opponent_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        if not selected_object:
            return
        target=selected_object[0]
        if target not in opponent.battlefield or target.get_flag("die") or target.get_flag("exile"):
            return
        player.action_store.start_record()
        try:
            damage=6 if target.state[0]>=4 else 3
            await self.attact_to_object(target,damage,"rgba(243, 0, 0, 0.9)","Missile_Hit")
        finally:
            player.action_store.end_record()
