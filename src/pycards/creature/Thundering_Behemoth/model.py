
from __future__ import annotations
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object

from game.buffs import KeyBuff

class Thundering_Behemoth(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Thundering Behemoth"
        self.live:int=5
        self.power:int=6
        self.actual_live:int=5
        self.actual_power:int=6

        self.type_creature:str="Beast Creature - Beast"
        self.type:str="Creature"

        self.mana_cost:str="4GGG"
        self.color:str="green"
        self.type_card:str="Beast Creature - Beast"
        self.rarity:str="Rare"
        self.content:str="Trample (This creature can deal excess combat damage to the player or planeswalker it's attacking.), When Thundering Behemoth enters the battlefield, creatures you control gain trample until end of turn."
        self.image_path:str="cards/creature/Thundering Behemoth/image.jpg"

        self.flag_dict["Trample"]=True


    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        for creature in player.battlefield:
            buff = KeyBuff(self,creature,"Trample")
            buff.set_end_of_turn()
            creature.gain_buff(buff,self)
        