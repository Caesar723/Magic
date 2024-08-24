
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import KeyBuff

class Emberheart_Dragonrider(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Emberheart Dragonrider"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Human Knight Creature"
        self.type:str="Creature"

        self.mana_cost:str="1RR"
        self.color:str="red"
        self.type_card:str="Human Knight Creature"
        self.rarity:str="Rare"
        self.content:str="When Emberheart Dragonrider enters the battlefield, you may pay R. If you do, target creature gains haste until end of turn."
        self.image_path:str="cards/creature/Emberheart Dragonrider/image.jpg"

    @select_object("all_creatures",1)
    async def when_enter_battlefield(self,player:'Player',opponent:'Player',selected_object:tuple['Card']=()):
        if selected_object:
            cost={"colorless":0,"U":0,"W":0,"B":0,"R":1,"G":0}
            result=player.check_can_use(cost)
            if result[0]:
                await player.generate_and_consume_mana(result[1],cost,self)
                buff=KeyBuff(self,selected_object[0],"haste")
                buff.set_end_of_turn()
                selected_object[0].gain_buff(buff,self)
            

        