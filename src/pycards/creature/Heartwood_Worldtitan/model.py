from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Heartwood_Worldtitan(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=269

        self.name:str="Heartwood Worldtitan"
        self.live:int=10
        self.power:int=10
        self.actual_live:int=10
        self.actual_power:int=10
        self.type_creature:str="Creature - Treefolk Giant"
        self.type:str="Creature"
        self.mana_cost:str="6GGGG"
        self.color:str="green"
        self.type_card:str="Creature - Treefolk Giant"
        self.rarity:str="Mythic Rare"
        self.content:str="Trample. When Heartwood Worldtitan enters the battlefield, create two 3/3 green Beast creature tokens."
        self.image_path:str="cards/creature/Heartwood Worldtitan/image.jpg"
        self.flag_dict["Trample"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            for _ in range(2):
                player.append_card(Heartwood_Worldtitan_Beast(player),"battlefield")
        finally:
            player.action_store.end_record()


class Heartwood_Worldtitan_Beast(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Beast"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3
        self.type_creature:str="Creature - Beast"
        self.type:str="Creature"
        self.mana_cost:str=""
        self.color:str="green"
        self.type_card:str="Creature - Beast"
        self.rarity:str="Common"
        self.content:str=""
        self.image_path:str="cards/creature/Heartwood Worldtitan/image.jpg"
