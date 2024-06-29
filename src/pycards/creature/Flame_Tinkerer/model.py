
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object,send_select_request
from game.type_action import actions

class Flame_Tinkerer(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Flame Tinkerer"
        self.live:int=1
        self.power:int=2
        self.actual_live:int=1
        self.actual_power:int=2

        self.type_creature:str="Goblin Creature"
        self.type:str="Creature"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Goblin Creature"
        self.rarity:str="Common"
        self.content:str="When Flame Tinkerer enters the battlefield, you may pay R. If you do, it deals 1 damage to target creature."
        self.image_path:str="cards/creature/Flame Tinkerer/image.jpg"

    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None,selected_object:tuple['Card']=()):# when creature enter battlefield
        
        
        if selected_object and selected_object[0].content!="Do nothing":
            cost={"colorless":0,"U":0,"W":0,"B":0,"R":1,"G":0}
            result=player.check_can_use(cost)
            if result[0]:
                await player.generate_and_consume_mana(result[1],cost,self)
                #player.action_store.add_action(actions.Change_Mana(self,player,player.get_manas()))
                player.action_store.start_record()
                await self.attact_to_object(selected_object[0],1,"rgba(243, 0, 0, 0.9)","Missile_Hit")
                player.action_store.end_record()
            



    async def selection_step(self, player: "Player" = None, opponent: "Player" = None,selection_random:bool=False):
        selection1=self.create_selection("Pay R",1)
        selection2=self.create_selection("Do nothing",2)
        card=await player.send_selection_cards([selection1,selection2],selection_random)
        print(card)
        if card!="cancel" and card.selection_index==1 :
            if  (player.battlefield or opponent.battlefield):
                creature=await send_select_request(self,"all_creatures",1,selection_random)
                if creature!="cancel":
                    return creature
                else:
                    return ["cancel"]
            return [selection2]
            
        return [card]


        