from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Worldpyre_Cataclysm(Sorcery):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=266

        self.name:str="Worldpyre Cataclysm"
        self.type:str="Sorcery"
        self.mana_cost:str="6RRR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Worldpyre Cataclysm deals 7 damage to each creature your opponent controls and 5 damage to your opponent."
        self.image_path:str="cards/sorcery/Worldpyre Cataclysm/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            for creature in list(opponent.battlefield):
                await self.attact_to_object(creature,7,"rgba(243, 0, 0, 0.9)","Missile_Hit")
            await self.attact_to_object(opponent,5,"rgba(243, 0, 0, 0.9)","Missile_Hit")
        finally:
            player.action_store.end_record()
