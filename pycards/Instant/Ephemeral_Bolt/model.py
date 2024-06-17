
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object,send_select_request


class Ephemeral_Bolt(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ephemeral Bolt"

        self.type:str="Instant"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Ephemeral Bolt deals 3 damage to target creature or player. If Ephemeral Bolt is in your graveyard, you may cast it for its flashback cost. If you do, exile it as it resolves."
        self.image_path:str="cards/Instant/Ephemeral Bolt/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:list['Card']=()):
        if selected_object:
            if len(selected_object)==2:
                cost={"colorless":2,"U":0,"W":0,"B":0,"R":1,"G":0}
                result=player.check_can_use(cost)
                if result[0]:
                    await player.generate_and_consume_mana(result[1],cost,self)
                else:
                    selected_object.pop()
            
            for obj in selected_object:
                player.action_store.start_record()
                await self.attact_to_object(obj,3,"rgba(243, 0, 0, 0.9)","Missile_Hit")
                player.action_store.end_record()

    async def selection_step(self, player: "Player" = None, opponent: "Player" = None):
        total_object=[]
        object_1=await send_select_request(self,"all_roles",1)
        if object_1=="cancel":
            return ["cancel"]
        total_object+=object_1

        selection1=self.create_selection("Pay 2R to flashback",1)
        selection2=self.create_selection("Do nothing",2)
        card=await player.send_selection_cards([selection1,selection2])

        if card=="cancel":
            return ["cancel"]
        elif card.selection_index==1:
            object_2=await send_select_request(self,"all_roles",1)
            if object_2=="cancel":
                return ["cancel"]
            total_object+=object_2
        return total_object

        