
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random

class Chaotic_Eruption(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=195

        self.name:str="Chaotic Eruption"

        self.type:str="Sorcery"

        self.mana_cost:str="2R"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Destroy target land. For each land destroyed this way, its controller randomly discard a card."
        self.image_path:str="cards/sorcery/Chaotic Eruption/image.jpg"

    @select_object("opponent_lands",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            target = selected_object[0]
            if target in opponent.land_area:
                await self.destroy_land(target, "rgba(255,0,0,1)", "Missile_Hit")
                if opponent.hand:
                    cards_to_discard=random.choice(opponent.hand)
                    opponent.discard(cards_to_discard)




        