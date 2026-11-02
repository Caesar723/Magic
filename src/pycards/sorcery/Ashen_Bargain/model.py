from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_action import actions


class Ashen_Bargain(Sorcery):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":2,"life_loss":2}

        self.fixed_id:int=246

        self.name:str="Ashen Bargain"
        self.type:str="Sorcery"
        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Draw {draw_count_word} card{draw_count_plural}, then you lose {life_loss} life."
        self.image_path:str="cards/sorcery/Ashen Bargain/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            player.draw_card(self.effect_params["draw_count"])
            player.life-=self.effect_params["life_loss"]
            player.action_store.add_action(actions.Attack_To_Object(player,player,player,"rgba(80, 0, 120, 0.9)","Missile_Hit",[player.life]))
            await player.check_dead()
        finally:
            player.action_store.end_record()
