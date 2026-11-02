from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Ashwing_Tyrant(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"damage":3}

        self.fixed_id:int=264

        self.name:str="Ashwing Tyrant"
        self.live:int=6
        self.power:int=7
        self.actual_live:int=6
        self.actual_power:int=7
        self.type_creature:str="Creature - Dragon"
        self.type:str="Creature"
        self.mana_cost:str="5RRR"
        self.color:str="red"
        self.type_card:str="Creature - Dragon"
        self.rarity:str="Mythic Rare"
        self.content:str="Flying. When Ashwing Tyrant enters the battlefield, it deals {damage} damage to your opponent."
        self.image_path:str="cards/creature/Ashwing Tyrant/image.jpg"
        self.flag_dict["flying"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            await self.attact_to_object(opponent,self.effect_params["damage"],"rgba(243, 0, 0, 0.9)","Missile_Hit")
        finally:
            player.action_store.end_record()
