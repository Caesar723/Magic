
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import Indestructible
import random

class Ancient_Stonewood(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ancient Stonewood"
        self.live:int=7
        self.power:int=5
        self.actual_live:int=7
        self.actual_power:int=5

        self.type_creature:str="Creature - Treefolk"
        self.type:str="Creature"

        self.mana_cost:str="4GG"
        self.color:str="green"
        self.type_card:str="Creature - Treefolk"
        self.rarity:str="Rare"
        self.content:str="Indestructible. Whenever Ancient Stonewood is dealt damage, it deals that much damage to random creature an opponent controls."
        self.image_path:str="cards/creature/Ancient Stonewood/image.jpg"



        buff_indestructible=Indestructible(self,self)
        self.buffs.append(buff_indestructible)
        self.update_buff()


    async def when_hurt(self,card:"Creature",value:int,player: "Player" = None, opponent: "Player" = None):#当受到伤害时 OK
        super().when_hurt(card,value,player,opponent)
        if opponent.battlefield:
            card_opponent=random.choice(opponent.battlefield)
            await self.attact_to_object(card_opponent,value,"rgba(10, 243, 10, 0.9)","Missile_Hit")

