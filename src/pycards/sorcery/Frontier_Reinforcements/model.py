from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_cards.creature import Creature


class Frontier_Reinforcements(Sorcery):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=247

        self.name:str="Frontier Reinforcements"
        self.type:str="Sorcery"
        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="If you control no creatures, create two 1/2 green Scout creature tokens. Otherwise, create one 1/2 green Scout creature token."
        self.image_path:str="cards/sorcery/Frontier Reinforcements/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            count=2 if not player.battlefield else 1
            for _ in range(count):
                player.append_card(Frontier_Reinforcements_Scout(player),"battlefield")
        finally:
            player.action_store.end_record()


class Frontier_Reinforcements_Scout(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Scout"
        self.live:int=2
        self.power:int=1
        self.actual_live:int=2
        self.actual_power:int=1
        self.type_creature:str="Creature - Scout"
        self.type:str="Creature"
        self.mana_cost:str=""
        self.color:str="green"
        self.type_card:str="Creature - Scout"
        self.rarity:str="Common"
        self.content:str=""
        self.image_path:str="cards/sorcery/Frontier Reinforcements/image.jpg"
