from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Emberforge_Raider(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"damage":1}

        self.fixed_id:int=251

        self.name:str="Emberforge Raider"
        self.live:int=3
        self.power:int=4
        self.actual_live:int=3
        self.actual_power:int=4
        self.type_creature:str="Creature - Human Warrior"
        self.type:str="Creature"
        self.mana_cost:str="2RR"
        self.color:str="red"
        self.type_card:str="Creature - Human Warrior"
        self.rarity:str="Uncommon"
        self.content:str="Haste. When Emberforge Raider enters the battlefield, it deals {damage} damage to your opponent."
        self.image_path:str="cards/creature/Emberforge Raider/image.jpg"
        self.flag_dict["haste"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            await self.attact_to_object(opponent,self.effect_params["damage"],"rgba(243, 0, 0, 0.9)","Missile_Hit")
        finally:
            player.action_store.end_record()
