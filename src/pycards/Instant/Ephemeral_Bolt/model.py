
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object,send_select_request


class Ephemeral_Bolt(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=19

        self.name:str="Ephemeral Bolt"

        self.type:str="Instant"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Ephemeral Bolt deals 1 damage to target creature or player. If a creature dealt damage this way dies this turn, you may draw a card."
        self.image_path:str="cards/Instant/Ephemeral Bolt/image.jpg"

    @select_object("all_roles",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:list['Card']=()):
        if selected_object:
            await self.attact_to_object(selected_object[0],1,"rgba(255,0,0,0.9)","Missile_Hit")
            player.draw_card(1)

   

        