
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.type_action.actions import Change_Mana

class Mystic_Convergence(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystic Convergence"

        self.type:str="Instant"

        self.mana_cost:str="2GW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Prevent all combat damage that would be dealt this turn. At the beginning of your next main phase, add X mana in any combination of colors to your mana pool, where X is the amount of combat damage prevented this way."
        self.image_path:str="cards/Instant/Mystic Convergence/image.jpg"

        self.damage_collect=0


    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        self.flag_dict["start_receive"]=True

    async def when_an_object_hert(self,object:"Player|Creature",value:int,player: "Player" = None, opponent: "Player" = None):#当一个card or 人物收到伤害，object是card 或者 player
        #print(player.room.get_flag("attacker_defenders") , self.get_flag("start_receive"))
        if player.room.get_flag("attacker_defenders") and self.get_flag("start_receive"):
            await self.cure_to_object(object,value,"rgba(89,154,85,0.6)","Missile_Hit")
            self.damage_collect+=value

    async def when_start_turn(self,player: "Player" = None, opponent: "Player" = None):#OK
        if self.get_flag("start_receive"):
            average=int(self.damage_collect/5)
            player.mana["G"]+=average
            player.mana["U"]+=average
            player.mana["W"]+=average
            player.mana["B"]+=average
            player.mana["R"]+=(self.damage_collect-4*average)
            player.action_store.add_action(Change_Mana(self,player,player.get_manas()))
            
        self.flag_dict["start_receive"]=False

            

        