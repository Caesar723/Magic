from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_cards.creature import Creature


class Verdant_Stampede(Sorcery):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"token_power":4,"token_toughness":4,"token_count":3}

        self.fixed_id:int=267

        self.name:str="Verdant Stampede"
        self.type:str="Sorcery"
        self.mana_cost:str="6GGG"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Create {token_count_word} {token_power}/{token_toughness} green Beast creature token{token_count_plural} with trample."
        self.image_path:str="cards/sorcery/Verdant Stampede/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            for _ in range(self.effect_params["token_count"]):
                token=self.create_token(Verdant_Stampede_Beast,player)
                player.append_card(token,"battlefield")
        finally:
            player.action_store.end_record()


class Verdant_Stampede_Beast(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={}

        self.name:str="Beast"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4
        self.type_creature:str="Creature - Beast"
        self.type:str="Creature"
        self.mana_cost:str=""
        self.color:str="green"
        self.type_card:str="Creature - Beast"
        self.rarity:str="Common"
        self.content:str="trample."
        self.image_path:str="cards/sorcery/Verdant Stampede/image.jpg"
        self.flag_dict["Trample"]=True
