
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object,send_select_request


class Flameblade_Pyromancer(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Flameblade Pyromancer"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Shaman"
        self.type:str="Creature"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Human Shaman"
        self.rarity:str="Uncommon"
        self.content:str="When Flameblade Pyromancer enters the battlefield, you may discard a card. If you do, it deals 2 damage to target creature or player."
        self.image_path:str="cards/creature/Flameblade Pyromancer/image.jpg"

    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None,selected_object:tuple['Card']=()):# when creature enter battlefield
        
        
        if selected_object and (isinstance(selected_object[0],type(player)) or selected_object[0].content!="Do nothing"):
            #player.action_store.add_action(actions.Change_Mana(self,player,player.get_manas()))
            player.action_store.start_record()
            await self.attact_to_object(selected_object[0],2,"rgba(243, 0, 0, 0.9)","Missile_Hit")
            player.action_store.end_record()
            



    async def selection_step(self, player: "Player" = None, opponent: "Player" = None,selection_random:bool=False):
        selection1=self.create_selection("Discard a card",1)
        selection2=self.create_selection("Do nothing",2)
        card=await player.send_selection_cards([selection1,selection2],selection_random)
        print(card)
        if card!="cancel" and card.selection_index==1 :
            
            discard_list=list(player.hand)
            if self in discard_list:
                discard_list.remove(self)
            if discard_list:
                discard=await player.send_selection_cards(discard_list,selection_random)
                if discard !="cancel":
                    
                    player.discard(discard)

                    creature=await send_select_request(self,"all_roles",1,selection_random)
                    if creature!="cancel":
                        return creature
                    else:
                        return ["cancel"]
                else:
                    return ["cancel"]
            


            return [selection2]
            
        return [card]
    



        