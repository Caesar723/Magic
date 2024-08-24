
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import StateBuff

class Luminous_Angel(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Luminous Angel"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Angel Creature - Angel"
        self.type:str="Creature"

        self.mana_cost:str="3WW"
        self.color:str="gold"
        self.type_card:str="Angel Creature - Angel"
        self.rarity:str="Rare"
        self.content:str="Flying, Lifelink (Damage dealt by this creature also causes you to gain that much life.), At the beginning of your upkeep, if you have at least 20 or more life, gain +1/+1"
        self.image_path:str="cards/creature/Luminous Angel/image.jpg"
        self.flag_dict["lifelink"]=True
        self.flag_dict["flying"]=True


    async def when_start_turn(self,player: "Player" = None, opponent: "Player" = None):
        if player.life>=20 and self in player.battlefield:
            buff=StateBuff(self,self,1,1)
            self.gain_buff(buff,self)


        