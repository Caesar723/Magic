from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_cards.creature import Creature


class Radiant_Procession(Sorcery):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"token_power":2,"token_toughness":2,"token_count":3}

        self.fixed_id:int=257

        self.name:str="Radiant Procession"
        self.type:str="Sorcery"
        self.mana_cost:str="3WWW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Create {token_count_word} {token_power}/{token_toughness} white Knight creature token{token_count_plural} with vigilance."
        self.image_path:str="cards/sorcery/Radiant Procession/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            for _ in range(self.effect_params["token_count"]):
                token=self.create_token(Radiant_Procession_Knight,player)
                player.append_card(token,"battlefield")
        finally:
            player.action_store.end_record()


class Radiant_Procession_Knight(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={}

        self.name:str="Knight"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2
        self.type_creature:str="Creature - Knight"
        self.type:str="Creature"
        self.mana_cost:str=""
        self.color:str="gold"
        self.type_card:str="Creature - Knight"
        self.rarity:str="Common"
        self.content:str="vigilance."
        self.image_path:str="cards/sorcery/Radiant Procession/image.jpg"
        self.flag_dict["Vigilance"]=True
