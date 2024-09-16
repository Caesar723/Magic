
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Timeless_Intervention(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Timeless Intervention"

        self.type:str="Instant"

        self.mana_cost:str="4GW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Exile all creatures and planeswalkers. Return all exiled creatures and planeswalkers to the battlefield under their owners' control at the beginning of the next end step."
        self.image_path:str="cards/Instant/Timeless Intervention/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        for creature_self in player.battlefield:
            await self.exile_object(creature_self,"rgba(255,255,0,0.7)","Missile_Hit")
        for creature_oppo in opponent.battlefield:
            await self.exile_object(creature_oppo,"rgba(255,255,0,0.7)","Missile_Hit")

        self.flag_dict["return_creature"]=True
    async def when_start_turn(self,player: "Player" = None, opponent: "Player" = None):#OK
        if self.get_flag("return_creature"):
            for creature_self in player.get_cards_by_pos_type("exile_area",Creature):
                player.remove_card(creature_self,"exile_area")
                new_creature_self=type(creature_self)(player)
                player.append_card(new_creature_self,"battlefield")
                
            for creature_oppo in opponent.get_cards_by_pos_type("exile_area",Creature): 
                opponent.remove_card(creature_oppo,"exile_area")
                new_creature_self=type(creature_oppo)(opponent)
                opponent.append_card(new_creature_self,"battlefield")
                
        self.flag_dict["return_creature"]=False

    