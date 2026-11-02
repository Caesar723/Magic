from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object
import random


class Mistbound_Archivist(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":2,"discard_count":1}

        self.fixed_id:int=253

        self.name:str="Mistbound Archivist"
        self.live:int=4
        self.power:int=2
        self.actual_live:int=4
        self.actual_power:int=2
        self.type_creature:str="Creature - Human Wizard"
        self.type:str="Creature"
        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Creature - Human Wizard"
        self.rarity:str="Rare"
        self.content:str="When Mistbound Archivist enters the battlefield, draw {draw_count_word} card{draw_count_plural}, then discard {discard_count_article} card{discard_count_plural} at random."
        self.image_path:str="cards/creature/Mistbound Archivist/image.jpg"

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            player.draw_card(self.effect_params["draw_count"])
            for _ in range(self.effect_params["discard_count"]):
                if player.hand:
                    discarded=random.choice(player.hand)
                    player.discard(discarded)
                    player.append_card(discarded,"graveyard")
        finally:
            player.action_store.end_record()
