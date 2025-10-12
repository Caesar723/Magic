
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Deep_Sea_Behemoth(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Deep Sea Behemoth"
        self.live:int=7
        self.power:int=7
        self.actual_live:int=7
        self.actual_power:int=7

        self.type_creature:str="Creature - Leviathan"
        self.type:str="Creature"

        self.mana_cost:str="6UU"
        self.color:str="blue"
        self.type_card:str="Creature - Leviathan"
        self.rarity:str="Rare"
        self.content:str="When Deep Sea Behemoth enters the battlefield, gain control of target creature for as long as you control Deep Sea Behemoth."
        self.image_path:str="cards/creature/Deep Sea Behemoth/image.jpg"

        self.control_creature=None



    @select_object("opponent_creatures",1)
    async def when_enter_battlefield(self,player:Player,opponent:Player,selected_object:tuple["Card"]):
        if selected_object:
            self.control_creature=selected_object[0]
            
            
            opponent.change_position(self.control_creature,player,-1)


    async def when_die(self,player:Player,opponent:Player,name:str="battlefield"):
        if self.control_creature and self.control_creature in self.player.battlefield:
            
            player.change_position(self.control_creature,opponent,-1)
            
           