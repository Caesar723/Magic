
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Luminous_Guardian(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Luminous Guardian"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Angel Creature - Angel"
        self.type:str="Creature"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Angel Creature - Angel"
        self.rarity:str="Rare"
        self.content:str="Flying, Lifelink (Damage dealt by this creature also causes you to gain that much life), When Luminous Guardian enters the battlefield, you may exile target creature with power 3 or greater an opponent controls until Luminous Guardian leaves the battlefield."
        self.image_path:str="cards/creature/Luminous Guardian/image.jpg"


        self.flag_dict['lifelink']=True
        self.flag_dict['flying']=True

        self.card_store=False
        
    @select_object("all_creatures",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object and selected_object[0].state[0]>=3:
            await self.exile_object(selected_object[0],"rgba(255,215,0,0.5)","Missile_Hit")
            self.card_store=selected_object[0]

    async def when_leave_battlefield(self,player: "Player" = None, opponent: "Player" = None,name:str='battlefield'):
        await super().when_leave_battlefield(player,opponent,name)
        if self.card_store:
            self.card_store.player.remove_card(self.card_store,"exile_area")
            new_card=type(self.card_store)(self.card_store.player)
            self.card_store.player.append_card(new_card,"battlefield")
            self.card_store=False