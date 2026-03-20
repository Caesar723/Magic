
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Shadowstrike(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=64

        self.name:str="Shadowstrike"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Destroy target tapped creature. If a creature was destroyed this way, you may draw a card."
        self.image_path:str="cards/Instant/Shadowstrike/image.jpg"


    @select_object("all_creatures",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        if selected_object:
            if selected_object[0].get_flag("tap"):
                await self.destroy_object(selected_object[0],"rgba(0,0,0,0.5)","Missile_Hit")
            player.draw_card(1)
        