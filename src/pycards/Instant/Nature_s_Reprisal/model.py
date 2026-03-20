
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Nature_s_Reprisal(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Nature's Reprisal"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Destroy target artifact or enchantment."
        self.image_path:str="cards/Instant/Nature's Reprisal/image.jpg"

    @select_object("opponent_permanents",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            await self.destroy_object(selected_object[0], "rgba(255,0,0,0.5)", "Missile_Hit")




        