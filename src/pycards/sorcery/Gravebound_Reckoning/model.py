from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Gravebound_Reckoning(Sorcery):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=256

        self.name:str="Gravebound Reckoning"
        self.type:str="Sorcery"
        self.mana_cost:str="3BB"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Destroy target creature an opponent controls. You gain 3 life."
        self.image_path:str="cards/sorcery/Gravebound Reckoning/image.jpg"

    @select_object("opponent_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        if not selected_object:
            return
        target=selected_object[0]
        if target not in opponent.battlefield or target.get_flag("die") or target.get_flag("exile"):
            return
        player.action_store.start_record()
        try:
            await self.destroy_object(target,"rgba(80, 0, 120, 0.9)","Missile_Hit")
            await self.cure_to_object(player,3,"rgba(100, 220, 140, 0.9)","Cure")
        finally:
            player.action_store.end_record()
