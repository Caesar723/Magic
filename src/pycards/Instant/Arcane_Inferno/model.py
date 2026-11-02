
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Arcane_Inferno(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"damage":3,"damage_high":5,"power_threshold":5}

        self.fixed_id:int=3

        self.name:str="Arcane Inferno"

        self.type:str="Instant"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Arcane Inferno deals {damage} damage to any target. If you control a creature with power {power_threshold} or greater, Arcane Inferno deals {damage_high} damage instead."
        self.image_path:str="cards/Instant/Arcane Inferno/image.jpg"

    @select_object("all_roles",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        if selected_object:
            power=self.effect_params["damage"]
            for creature in player.battlefield:
                state=creature.state
                if state[0]>=self.effect_params["power_threshold"]:
                    power=self.effect_params["damage_high"]
            

            player.action_store.start_record()
            await self.attact_to_object(selected_object[0],power,"rgba(243, 0, 0, 0.9)","Missile_Hit")
            player.action_store.end_record()


        