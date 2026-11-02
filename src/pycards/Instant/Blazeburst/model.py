
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Blazeburst(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"damage":3}

        self.fixed_id:int=10

        self.name:str="Blazeburst"

        self.type:str="Instant"

        self.mana_cost:str="1RR"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Blazeburst deals {damage} damage to any target."
        self.image_path:str="cards/Instant/Blazeburst/image.jpg"

    @select_object("all_roles",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        if selected_object:
            await self.attact_to_object(selected_object[0],self.effect_params["damage"],"rgba(243, 0, 0, 0.9)","Missile_Hit")


        