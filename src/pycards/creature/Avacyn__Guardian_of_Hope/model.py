
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import Indestructible

class Avacyn__Guardian_of_Hope(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Avacyn, Guardian of Hope"
        self.live:int=4
        self.power:int=5
        self.actual_live:int=4
        self.actual_power:int=5

        self.type_creature:str="Angel Creature"
        self.type:str="Creature"

        self.mana_cost:str="3W"
        self.color:str="gold"
        self.type_card:str="Angel Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="Flying, Vigilance, Lifelink. When Avacyn, Guardian of Hope enters the battlefield, creatures you control gain indestructible until end of turn."
        self.image_path:str="cards/creature/Avacyn, Guardian of Hope/image.jpg"


        self.flag_dict['lifelink']=True
        self.flag_dict['flying']=True
        self.flag_dict["Vigilance"]=True

    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        for creature in player.battlefield:
            buff=Indestructible(self,creature)
            buff.set_end_of_turn()
            creature.gain_buff(buff,self)