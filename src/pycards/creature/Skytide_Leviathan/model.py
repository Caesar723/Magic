from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Skytide_Leviathan(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=260

        self.name:str="Skytide Leviathan"
        self.live:int=6
        self.power:int=5
        self.actual_live:int=6
        self.actual_power:int=5
        self.type_creature:str="Creature - Leviathan"
        self.type:str="Creature"
        self.mana_cost:str="4UUU"
        self.color:str="blue"
        self.type_card:str="Creature - Leviathan"
        self.rarity:str="Rare"
        self.content:str="Flying. When Skytide Leviathan enters the battlefield, draw two cards."
        self.image_path:str="cards/creature/Skytide Leviathan/image.jpg"
        self.flag_dict["flying"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            player.draw_card(2)
        finally:
            player.action_store.end_record()
