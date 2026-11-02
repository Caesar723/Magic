from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Rootwatch_Guardian(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"heal":2}

        self.fixed_id:int=252

        self.name:str="Rootwatch Guardian"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4
        self.type_creature:str="Creature - Treefolk"
        self.type:str="Creature"
        self.mana_cost:str="2GG"
        self.color:str="green"
        self.type_card:str="Creature - Treefolk"
        self.rarity:str="Uncommon"
        self.content:str="Reach. When Rootwatch Guardian enters the battlefield, you gain {heal} life."
        self.image_path:str="cards/creature/Rootwatch Guardian/image.jpg"
        self.flag_dict["reach"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            await self.cure_to_object(player,self.effect_params["heal"],"rgba(100, 220, 140, 0.9)","Cure")
        finally:
            player.action_store.end_record()
