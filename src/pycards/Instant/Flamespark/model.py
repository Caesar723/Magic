
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

        self.name:str="Flamespark"

        self.type:str="Instant"

        self.mana_cost:str="1RR"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Flamespark deals 3 damage to any target. If you control a Mountain, it deals 5 damage instead."
        self.image_path:str="cards/Instant/Flamespark/image.jpg"

    @select_object("all_roles",1)
    async def when_enter_battlefield(self,player:'Player',opponent:'Player',selected_object:tuple['Card']=()):
        damage=3
        if selected_object:
            for land in player.land_area:
                if isinstance(land,Mountain):
                    damage=5
            await self.attact_to_object(selected_object[0],damage,"rgba(255,0,0,1)","Missile_Hit")
        