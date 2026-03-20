
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Storm_Bringer(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=144

        self.name:str="Storm Bringer"
        self.live:int=5
        self.power:int=5
        self.actual_live:int=5
        self.actual_power:int=5

        self.type_creature:str="Creature - Elemental"
        self.type:str="Creature"

        self.mana_cost:str="4UU"
        self.color:str="blue"
        self.type_card:str="Creature - Elemental"
        self.rarity:str="Rare"
        self.content:str="Flying. When Storm Bringer enters the battlefield, it deals 3 damage to each opponent and you gain 3 life."
        self.image_path:str="cards/creature/Storm Bringer/image.jpg"


        self.flag_dict["flying"]=True


    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):


        for card in opponent.battlefield:
            await self.attact_to_object(card,3,self.random_blue_rgba(),"Cure")
        await self.attact_to_object(opponent,3,self.random_blue_rgba(),"Cure")
        await self.cure_to_object(player,3,"rgba(100, 243, 100, 0.9)","Cure")

        
    def random_blue_rgba(self,alpha=0.9):
        # 生成蓝色调（R、G 比较低，B 较高）
        r = random.randint(0, 100)      # 红色分量偏低
        g = random.randint(0, 150)      # 绿色分量中等
        b = random.randint(150, 255)    # 蓝色分量高
        return f"rgba({r}, {g}, {b}, {alpha})"