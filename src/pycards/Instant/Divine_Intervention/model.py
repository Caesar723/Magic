
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Divine_Intervention(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=15

        self.name:str="Divine Intervention"

        self.type:str="Instant"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Choose up to two target creatures. Prevent all damage that would be dealt to those creatures this turn. Gain life equal to the total damage prevented this way."
        self.image_path:str="cards/Instant/Divine Intervention/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        all_permanents = list(player.battlefield) + list(opponent.battlefield)
        for perm in all_permanents:
            await self.exile_object(perm, "rgba(239, 228, 83, 0.8)", "Missile_Hit")




        