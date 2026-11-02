
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import StateBuff


class Soul_Devourer(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"power_bonus":1,"toughness_bonus":1}

        self.name:str="Soul Devourer"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Creature - Demon"
        self.type:str="Creature"

        self.mana_cost:str="4BB"
        self.color:str="black"
        self.type_card:str="Creature - Demon"
        self.rarity:str="Rare"
        self.content:str="Whenever a creature dies, Soul Devourer gets +{power_bonus}/+{toughness_bonus} counters equal to the power of that creature."
        self.image_path:str="cards/creature/Soul Devourer/image.jpg"



    async def when_a_creature_die(self,creature:"Creature",player: "Player" = None, opponent: "Player" = None):#当随从死亡时（放入一个死亡随从的参数）
        if self in player.battlefield:
            power,live=creature.state
            for i in range(power):
                buff=StateBuff(self,self,self.effect_params["power_bonus"],self.effect_params["toughness_bonus"])
                buff.buff_missile="Cure"
                buff.color_missile="rgba(10, 10, 10, 0.9)"
                self.gain_buff(buff,self)