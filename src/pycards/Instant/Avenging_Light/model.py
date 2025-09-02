
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Avenging_Light(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Avenging Light"

        self.type:str="Instant"

        self.mana_cost:str="3W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Exile target nonland permanent. If it was a creature, you gain life equal to its power."
        self.image_path:str="cards/Instant/Avenging Light/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        if selected_object:
            await self.exile_object(selected_object[0],"rgba(255,255,0,0.7)","Missile_Hit")
            power=selected_object[0].state[0]
            await self.cure_to_object(player,power,"rgba(89,154,85,0.6)","Missile_Hit")

        