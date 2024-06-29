
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Emberheart_Salamander(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Emberheart Salamander"
        self.live:int=2
        self.power:int=4
        self.actual_live:int=2
        self.actual_power:int=4

        self.type_creature:str="Salamander Creature - Salamander"
        self.type:str="Creature"

        self.mana_cost:str="2RR"
        self.color:str="red"
        self.type_card:str="Salamander Creature - Salamander"
        self.rarity:str="Uncommon"
        self.content:str="Trample (This creature can deal excess combat damage to the player or planeswalker it's attacking.), When Emberheart Salamander enters the battlefield, it deals 2 damage to any target."
        self.image_path:str="cards/creature/Emberheart Salamander/image.jpg"

        self.flag_dict["Trample"]=True

    @select_object("all_roles",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None,selected_object:tuple['Card']=()):# when creature enter battlefield
        
        if selected_object:

            await self.attact_to_object(selected_object[0],2,"rgba(243, 0, 0, 0.9)","Missile_Hit")
    
        