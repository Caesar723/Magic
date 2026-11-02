from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Thorncrown_Ancient(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=262

        self.name:str="Thorncrown Ancient"
        self.live:int=7
        self.power:int=7
        self.actual_live:int=7
        self.actual_power:int=7
        self.type_creature:str="Creature - Treefolk"
        self.type:str="Creature"
        self.mana_cost:str="4GGG"
        self.color:str="green"
        self.type_card:str="Creature - Treefolk"
        self.rarity:str="Rare"
        self.content:str="Trample. When Thorncrown Ancient enters the battlefield, create two 1/1 green Scout creature tokens."
        self.image_path:str="cards/creature/Thorncrown Ancient/image.jpg"
        self.flag_dict["Trample"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            for _ in range(2):
                player.append_card(Thorncrown_Ancient_Scout(player),"battlefield")
        finally:
            player.action_store.end_record()


class Thorncrown_Ancient_Scout(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Scout"
        self.live:int=1
        self.power:int=1
        self.actual_live:int=1
        self.actual_power:int=1
        self.type_creature:str="Creature - Scout"
        self.type:str="Creature"
        self.mana_cost:str=""
        self.color:str="green"
        self.type_card:str="Creature - Scout"
        self.rarity:str="Common"
        self.content:str=""
        self.image_path:str="cards/creature/Thorncrown Ancient/image.jpg"
