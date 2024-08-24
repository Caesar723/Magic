
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import StateBuff
from game.type_cards.instant import Instant
from game.type_cards.sorcery import Sorcery

class Ralgar__the_Inferno_King__(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ralgar, the Inferno King"
        self.live:int=4
        self.power:int=5
        self.actual_live:int=4
        self.actual_power:int=5

        self.type_creature:str="Elemental Creature"
        self.type:str="Creature"

        self.mana_cost:str="3RR"
        self.color:str="colorless"
        self.type_card:str="Elemental Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="When Ralgar enters the battlefield, it deals 3 damage to any target. Whenever you cast an instant or sorcery spell, Ralgar gets +1/+0 until end of turn."
        self.image_path:str="cards/creature/Ralgar, the Inferno King  /image.jpg"

    @select_object("all_roles",1)
    async def when_enter_battlefield(self,player:'Player',opponent:'Player',selected_object:tuple['Card']=()):
        if selected_object:
            await self.attact_to_object(selected_object[0],3,"rgba(255,0,0,1)","Missile_Hit")

    async def when_play_a_card(self,card:'Card',player:'Player',opponent:'Player'):
        if (isinstance(card,Instant) or isinstance(card,Sorcery)) and self in player.battlefield:
            buff=StateBuff(self,self,1,0)
            self.gain_buff(buff,self)



            

        