
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Voidwisp_Harbinger(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Voidwisp Harbinger"
        self.live:int=4
        self.power:int=2
        self.actual_live:int=4
        self.actual_power:int=2

        self.type_creature:str="Spirit Creature - Spirit"
        self.type:str="Creature"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Spirit Creature - Spirit"
        self.rarity:str="Rare"
        self.content:str="Flash, Flying, When Voidwisp Harbinger enters the battlefield, you may scry 2. (To scry 2, look at the top two cards of your library, then put any number of them on the bottom of your library and the rest on top in any order.)"
        self.image_path:str="cards/creature/Voidwisp Harbinger/image.jpg"

        self.flag_dict["flying"]=True
        self.flag_dict["Flash"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:'Player',opponent:'Player',selected_object:tuple['Card']=()):
        await self.Scry(player,opponent,2)

        