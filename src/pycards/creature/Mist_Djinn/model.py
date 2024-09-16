
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Mist_Djinn(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mist Djinn"
        self.live:int=6
        self.power:int=4
        self.actual_live:int=6
        self.actual_power:int=4

        self.type_creature:str="Creature - Djinn"
        self.type:str="Creature"

        self.mana_cost:str="5UU"
        self.color:str="blue"
        self.type_card:str="Creature - Djinn"
        self.rarity:str="Rare"
        self.content:str="Mist Djinn can block any number of creatures."
        self.image_path:str="cards/creature/Mist Djinn/image.jpg"

    async def when_finish_defend(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#OK
        pass

        