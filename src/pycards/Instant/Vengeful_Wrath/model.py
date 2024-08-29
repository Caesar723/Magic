
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Vengeful_Wrath(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Vengeful Wrath"

        self.type:str="Instant"

        self.mana_cost:str="3BB"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Destroy target creature. Deal damage equal to its power to a random creature your opponent controls."
        self.image_path:str="cards/Instant/Vengeful Wrath/image.jpg"


    @select_object("all_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object[0]:
            player.action_store.start_record()
            power,life=selected_object[0].state
            await self.destroy_object(selected_object[0],"rgba(0,0,0,0.5)","Missile_Hit")
            
            if opponent.battlefield:
                creatures=random.choice(opponent.battlefield)
                player.action_store.start_record()
                await self.attact_to_object(creatures,power,"rgba(0,0,0,0.5)","Missile_Hit")
                player.action_store.end_record()
            player.action_store.end_record()




        