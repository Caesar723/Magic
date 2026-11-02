from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_action import actions


class Nightfall_Harvest(Sorcery):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"life_loss":3}

        self.fixed_id:int=263

        self.name:str="Nightfall Harvest"
        self.type:str="Sorcery"
        self.mana_cost:str="5BBB"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Destroy all creatures your opponent controls. You lose {life_loss} life."
        self.image_path:str="cards/sorcery/Nightfall Harvest/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            for creature in list(opponent.battlefield):
                await self.destroy_object(creature,"rgba(80, 0, 120, 0.9)","Missile_Hit")
            player.life-=self.effect_params["life_loss"]
            player.action_store.add_action(actions.Attack_To_Object(player,player,player,"rgba(80, 0, 120, 0.9)","Missile_Hit",[player.life]))
            await player.check_dead()
        finally:
            player.action_store.end_record()
