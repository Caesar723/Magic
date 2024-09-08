
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Dragon_Lord(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Dragon Lord"
        self.live:int=6
        self.power:int=6
        self.actual_live:int=6
        self.actual_power:int=6

        self.type_creature:str="Creature - Dragon"
        self.type:str="Creature"

        self.mana_cost:str="6RR"
        self.color:str="red"
        self.type_card:str="Creature - Dragon"
        self.rarity:str="Rare"
        self.content:str="Flying. Whenever Dragon Lord deals damage to an opponent, create two 4/4 red Dragon creature tokens."
        self.image_path:str="cards/creature/Dragon Lord/image.jpg"
        self.flag_dict["flying"]=True

    def summon_token(self):
        for i in range(2):  
            token=Dragon_Lord_Token(self.player)
            self.player.append_card(token,"battlefield")

    async def when_harm_is_done(self,card:"Creature|Player",value:int,player: "Player" = None, opponent: "Player" = None):#当造成伤害时 OK
        result= await super().when_harm_is_done(card,value,player,opponent)
        if card==opponent or card in opponent.battlefield:
            self.summon_token()
        return result
 

class Dragon_Lord_Token(Creature):
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Dragon Lord"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Creature - Dragon"
        self.type:str="Creature"

        self.mana_cost:str="R"
        self.color:str="red"
        self.type_card:str="Creature - Dragon"
        self.rarity:str="Rare"
        self.content:str=""
        self.image_path:str="cards/creature/Dragon Lord/image.jpg"
        