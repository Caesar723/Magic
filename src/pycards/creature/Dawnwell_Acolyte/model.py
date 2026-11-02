from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Dawnwell_Acolyte(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"heal":1}

        self.fixed_id:int=242

        self.name:str="Dawnwell Acolyte"
        self.live:int=2
        self.power:int=1
        self.actual_live:int=2
        self.actual_power:int=1
        self.type_creature:str="Creature - Human Cleric"
        self.type:str="Creature"
        self.mana_cost:str="W"
        self.color:str="gold"
        self.type_card:str="Creature - Human Cleric"
        self.rarity:str="Common"
        self.content:str="When Dawnwell Acolyte enters the battlefield, you gain {heal} life."
        self.image_path:str="cards/creature/Dawnwell Acolyte/image.jpg"

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            await self.cure_to_object(player,self.effect_params["heal"],"rgba(245, 238, 145, 0.8)","Cure")
        finally:
            player.action_store.end_record()
