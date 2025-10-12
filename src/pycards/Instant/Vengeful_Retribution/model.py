
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
import random


class Vengeful_Retribution(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Vengeful Retribution"

        self.type:str="Instant"

        self.mana_cost:str="4B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Opponent sacrifices two random creatures. If a creature was sacrificed this way, Vengeful Retribution deals damage to random target equal to the total power of the sacrificed creatures."
        self.image_path:str="cards/Instant/Vengeful Retribution/image.jpg"


    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if opponent.battlefield:
            creatures_opponent=list(opponent.battlefield)
            if len(opponent.battlefield)>=2:
                creatures=random.sample(creatures_opponent,2)
            else:
                creatures=creatures_opponent[0:1]

            total_power=sum(creature.state[0] for creature in creatures)
            for creature in creatures:
                await self.destroy_object(creature,"rgba(0,0,0,0.5)","Missile_Hit")

            rest_creatures=[c for c in creatures_opponent if c not in creatures]
            
            if rest_creatures:
                random_creature=random.choice(rest_creatures)
                await self.attact_to_object(random_creature,total_power,"rgba(0,0,0,0.5)","Missile_Hit")
    
        