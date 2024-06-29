
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

        self.name:str="Arcane Inferno"

        self.type:str="Instant"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Arcane Inferno deals 3 damage to any target. If you control a creature with power 5 or greater, Arcane Inferno deals 5 damage instead."
        self.image_path:str="cards/Instant/Arcane Inferno/image.jpg"

    @select_object("all_roles",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        if selected_object:
            power=3
            for creature in player.battlefield:
                state=creature.state
                if state[0]>=5:
                    power=5
            

            player.action_store.start_record()
            await self.attact_to_object(selected_object[0],power,"rgba(243, 0, 0, 0.9)","Missile_Hit")
            player.action_store.end_record()


        