
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.type_cards.creature import Creature
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Summoner_s_Respite(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=66

        self.name:str="Summoner's Respite"

        self.type:str="Instant"

        self.mana_cost:str="2GW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Prevent all combat damage that would be dealt this turn. You gain 4 life. Put a +1/+1 counter on each creature you control."
        self.image_path:str="cards/Instant/Summoner's Respite/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.buffs import StateBuff
        self.flag_dict["start_receive"]=True
        
        await self.cure_to_object(player, 4, "rgba(0,255,0,0.5)", "Missile_Hit")
        for creature in player.battlefield:
            buff = StateBuff(self, creature, 1, 1)
            creature.gain_buff(buff, self)

    async def when_an_object_hert(self,object:"Player|Creature",value:int,player: "Player" = None, opponent: "Player" = None):#当一个card or 人物收到伤害，object是card 或者 player
        #print(player.room.get_flag("attacker_defenders") , self.get_flag("start_receive"))
        if player.room.get_flag("attacker_defenders") and self.get_flag("start_receive"):
            await self.cure_to_object(object,value,"rgba(89,154,85,0.6)","Missile_Hit")
            self.damage_collect+=value


    async def when_start_turn(self,player: "Player" = None, opponent: "Player" = None):#OK
        self.flag_dict["start_receive"]=False

            
