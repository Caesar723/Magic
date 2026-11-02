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
        self.effect_params:dict={"token_power":1,"token_toughness":2,"token_count_empty":2,"token_count":1}

        self.fixed_id:int=247

        self.name:str="Frontier Reinforcements"
        self.type:str="Sorcery"
        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="If you control no creatures, create {token_count_empty_word} {token_power}/{token_toughness} green Scout creature token{token_count_empty_plural}. Otherwise, create {token_count_word} {token_power}/{token_toughness} green Scout creature token{token_count_plural}."
        self.image_path:str="cards/sorcery/Frontier Reinforcements/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            count=self.effect_params["token_count_empty"] if not player.battlefield else self.effect_params["token_count"]
            for _ in range(count):
                token=self.create_token(Frontier_Reinforcements_Scout,player)
                player.append_card(token,"battlefield")
        finally:
            player.action_store.end_record()


class Frontier_Reinforcements_Scout(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={}

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
