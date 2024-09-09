
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import StateBuff

class Kothar_the_Soul_Reaper(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Kothar the Soul Reaper"
        self.live:int=5
        self.power:int=5
        self.actual_live:int=5
        self.actual_power:int=5

        self.type_creature:str="Demon Creature"
        self.type:str="Creature"

        self.mana_cost:str="4B"
        self.color:str="black"
        self.type_card:str="Demon Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="When Kothar the Soul Reaper enters the battlefield, each opponent sacrifices a creature randomly. Whenever a creature dies, Kothar gets a +1/+1 counter."
        self.image_path:str="cards/creature/Kothar the Soul Reaper/image.jpg"


    @select_object("",1)
    async def when_enter_battlefield(self,player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if opponent.battlefield:    
            creature=random.choice(opponent.battlefield)
            await self.destroy_object(creature,"rgba(0,0,0,0.5)","Cure")

    async def when_a_creature_die(self,creature:"Creature",player: "Player" = None, opponent: "Player" = None):#当随从死亡时（放入一个死亡随从的参数）
        if self in player.battlefield:  
            buff=StateBuff(self,self,1,1)
            self.gain_buff(buff,self)