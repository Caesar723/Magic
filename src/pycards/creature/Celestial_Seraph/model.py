
from __future__ import annotations
from typing import TYPE_CHECKING, Union
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Celestial_Seraph(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Celestial Seraph"
        self.live:int=5
        self.power:int=5
        self.actual_live:int=5
        self.actual_power:int=5

        self.type_creature:str="Angel Creature - Angel"
        self.type:str="Creature"

        self.mana_cost:str="3WWW"
        self.color:str="gold"
        self.type_card:str="Angel Creature - Angel"
        self.rarity:str="Mythic Rare"
        self.content:str="Flying, Lifelink (Damage dealt by this creature also causes you to gain that much life), Whenever Celestial Seraph attacks, you may exile random nonland permanent an opponent controls until Celestial Seraph leaves the battlefield."
        self.image_path:str="cards/creature/Celestial Seraph/image.jpg"


        self.flag_dict['lifelink']=True
        self.flag_dict['flying']=True

        self.creature_store=[]

    async def when_start_attcak(self, card: "Creature | Player", player: "Player" = None, opponent: "Player" = None):
        creature=random.choice(opponent.battlefield)
        await self.exile_object(creature,"rgba(239, 228, 83, 0.8)","Missile_Hit")
        self.creature_store.append(creature)
        

    async def when_leave_battlefield(self, player: "Player" = None, opponent: "Player" = None, name: str = 'battlefield'):
        result= await super().when_leave_battlefield(player, opponent, name)
        for creature in self.creature_store:
            new_creature=type(creature)(opponent)
            opponent.append_card(new_creature,"battlefield")
        return result