
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from pycards.land.Mountain.model import Mountain

class Flamespark(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"damage":3,"damage_high":5}

        self.fixed_id:int=28

        self.name:str="Flamespark"

        self.type:str="Instant"

        self.mana_cost:str="1RR"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Flamespark deals {damage} damage to any target. If you control a Mountain, it deals {damage_high} damage instead."
        self.image_path:str="cards/Instant/Flamespark/image.jpg"

    @select_object("all_roles",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        damage=self.effect_params["damage"]
        if selected_object:
            for land in player.land_area:
                if isinstance(land,Mountain):
                    damage=self.effect_params["damage_high"]
            await self.attact_to_object(selected_object[0],damage,"rgba(255,0,0,1)","Missile_Hit")
        