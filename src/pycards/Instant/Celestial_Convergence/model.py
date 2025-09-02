
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Celestial_Convergence(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Celestial Convergence"

        self.type:str="Instant"

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Exile target permanent. If that permanent's mana value is 3 or less, its controller gains life equal to its mana value."
        self.image_path:str="cards/Instant/Celestial Convergence/image.jpg"


    @select_object("all_creatures",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        if selected_object:
            await self.exile_object(selected_object[0],"rgba(255,255,0,0.7)","Missile_Hit")
            mana=sum(selected_object[0].cost.values())
            if mana<=3:
                await self.cure_to_object(player,mana,"rgba(89,154,85,0.6)","Missile_Hit")
        