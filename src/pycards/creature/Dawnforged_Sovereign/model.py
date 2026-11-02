from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Dawnforged_Sovereign(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"heal":8,"token_power":2,"token_toughness":2,"token_count":2}

        self.fixed_id:int=270

        self.name:str="Dawnforged Sovereign"
        self.live:int=7
        self.power:int=7
        self.actual_live:int=7
        self.actual_power:int=7
        self.type_creature:str="Creature - Angel Noble"
        self.type:str="Creature"
        self.mana_cost:str="6WWWW"
        self.color:str="gold"
        self.type_card:str="Creature - Angel Noble"
        self.rarity:str="Mythic Rare"
        self.content:str="Flying, vigilance. When Dawnforged Sovereign enters the battlefield, you gain {heal} life and create {token_count_word} {token_power}/{token_toughness} white Knight creature token{token_count_plural}."
        self.image_path:str="cards/creature/Dawnforged Sovereign/image.jpg"
        self.flag_dict["flying"]=True
        self.flag_dict["Vigilance"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            await self.cure_to_object(player,self.effect_params["heal"],"rgba(245, 238, 145, 0.8)","Cure")
            for _ in range(self.effect_params["token_count"]):
                token=self.create_token(Dawnforged_Sovereign_Knight,player)
                player.append_card(token,"battlefield")
        finally:
            player.action_store.end_record()


class Dawnforged_Sovereign_Knight(Creature):

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
        self.image_path:str="cards/creature/Dawnforged Sovereign/image.jpg"
