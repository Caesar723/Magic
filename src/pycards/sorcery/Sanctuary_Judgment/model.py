from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_cards.creature import Creature


class Sanctuary_Judgment(Sorcery):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"token_power":2,"token_toughness":2,"token_count":2}

        self.fixed_id:int=265

        self.name:str="Sanctuary Judgment"
        self.type:str="Sorcery"
        self.mana_cost:str="5WWW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Destroy all creatures, then create {token_count_word} {token_power}/{token_toughness} white Knight creature token{token_count_plural}."
        self.image_path:str="cards/sorcery/Sanctuary Judgment/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            for creature in list(player.battlefield)+list(opponent.battlefield):
                await self.destroy_object(creature,"rgba(245, 238, 145, 0.8)","Missile_Hit")
            for _ in range(self.effect_params["token_count"]):
                token=self.create_token(Sanctuary_Judgment_Knight,player)
                player.append_card(token,"battlefield")
        finally:
            player.action_store.end_record()


class Sanctuary_Judgment_Knight(Creature):

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
        self.content:str=""
        self.image_path:str="cards/sorcery/Sanctuary Judgment/image.jpg"
