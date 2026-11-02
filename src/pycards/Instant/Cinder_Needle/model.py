from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Cinder_Needle(Instant):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"damage":2}

        self.fixed_id:int=244

        self.name:str="Cinder Needle"
        self.type:str="Instant"
        self.mana_cost:str="R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Cinder Needle deals {damage} damage to target creature an opponent controls."
        self.image_path:str="cards/Instant/Cinder Needle/image.jpg"

    @select_object("opponent_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        if not selected_object:
            return
        target=selected_object[0]
        if target not in opponent.battlefield or target.get_flag("die") or target.get_flag("exile"):
            return
        player.action_store.start_record()
        try:
            await self.attact_to_object(target,self.effect_params["damage"],"rgba(243, 0, 0, 0.9)","Missile_Hit")
        finally:
            player.action_store.end_record()
