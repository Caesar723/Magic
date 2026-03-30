
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Chaos_Unleashed(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=194

        self.name:str="Chaos Unleashed"

        self.type:str="Sorcery"

        self.mana_cost:str="1BR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Chaos Unleashed deals 3 damage to each creature and each player."
        self.image_path:str="cards/sorcery/Chaos Unleashed/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        for creature in list(player.battlefield) + list(opponent.battlefield):
            await self.attact_to_object(creature, 3, "rgba(255,0,0,1)", "Missile_Hit")
        await self.attact_to_object(player, 3, "rgba(255,0,0,1)", "Missile_Hit")
        await self.attact_to_object(opponent, 3, "rgba(255,0,0,1)", "Missile_Hit")

        