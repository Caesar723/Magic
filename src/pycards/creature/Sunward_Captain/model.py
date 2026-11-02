from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Sunward_Captain(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=255

        self.name:str="Sunward Captain"
        self.live:int=4
        self.power:int=3
        self.actual_live:int=4
        self.actual_power:int=3
        self.type_creature:str="Creature - Human Soldier"
        self.type:str="Creature"
        self.mana_cost:str="3WW"
        self.color:str="gold"
        self.type_card:str="Creature - Human Soldier"
        self.rarity:str="Rare"
        self.content:str="Vigilance. When Sunward Captain enters the battlefield, create two 1/1 white Soldier creature tokens."
        self.image_path:str="cards/creature/Sunward Captain/image.jpg"
        self.flag_dict["Vigilance"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            for _ in range(2):
                player.append_card(Sunward_Captain_Soldier(player),"battlefield")
        finally:
            player.action_store.end_record()


class Sunward_Captain_Soldier(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Soldier"
        self.live:int=1
        self.power:int=1
        self.actual_live:int=1
        self.actual_power:int=1
        self.type_creature:str="Creature - Soldier"
        self.type:str="Creature"
        self.mana_cost:str=""
        self.color:str="gold"
        self.type_card:str="Creature - Soldier"
        self.rarity:str="Common"
        self.content:str=""
        self.image_path:str="cards/creature/Sunward Captain/image.jpg"
