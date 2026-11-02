from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Tideglass_Recoil(Instant):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={}

        self.fixed_id:int=245

        self.name:str="Tideglass Recoil"
        self.type:str="Instant"
        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Return target creature an opponent controls to its owner's hand."
        self.image_path:str="cards/Instant/Tideglass Recoil/image.jpg"

    @select_object("opponent_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        if not selected_object:
            return
        target=selected_object[0]
        if target not in opponent.battlefield or target.get_flag("die") or target.get_flag("exile"):
            return
        player.action_store.start_record()
        try:
            owner=target.player
            owner.remove_card(target,"battlefield")
            owner.append_card(target.copy_for_player(owner),"hand")
        finally:
            player.action_store.end_record()
