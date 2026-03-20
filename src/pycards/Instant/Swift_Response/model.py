
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Swift_Response(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=67

        self.name:str="Swift Response"

        self.type:str="Instant"

        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Instantly destroy target attacking or blocking creature with power 2 or less."
        self.image_path:str="cards/Instant/Swift Response/image.jpg"

    @select_object("opponent_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object and selected_object[0].power <= 2:
            await self.destroy_object(selected_object[0], "rgba(255,0,0,0.5)", "Missile_Hit")




        