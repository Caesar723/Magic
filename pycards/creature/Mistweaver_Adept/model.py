
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Mistweaver_Adept(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mistweaver Adept"
        self.live:int=1
        self.power:int=2
        self.actual_live:int=1
        self.actual_power:int=2

        self.type_creature:str="Human Wizard"
        self.type:str="Creature"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Human Wizard"
        self.rarity:str="Uncommon"
        self.content:str="When Mistweaver Adept enters the battlefield, you may return target creature to its owner's hand. If you do, scry 2."
        self.image_path:str="cards/creature/Mistweaver Adept/image.jpg"

    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None,selected_object:tuple['Card']=()):# when creature enter battlefield
        
        print(selected_object[0].selection_index)
        if selected_object[0].selection_index==1:
            cost={"colorless":2,"U":0,"W":0,"B":0,"R":0,"G":0}
            result=player.check_can_use(cost)
            print(result)
            if result[0]:
                await player.generate_and_consume_mana(result[1],cost,self)


    async def selection_step(self, player: "Player" = None, opponent: "Player" = None):
        selection1=self.create_selection("scry 2-return target creature to its owner's hand",1)
        selection2=self.create_selection("Do nothing",2)
        card=await player.send_selection_cards([selection1,selection2])
        return [card]


        