
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object


class Paladin_s_Judging_Light(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Paladin's Judging Light"

        self.type:str="Instant"

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target spell. Its controller takes light damage equal to its mana cost."
        self.image_path:str="cards/Instant/Paladin's Judging Light/image.jpg"


    @select_object("",1)
    async def card_ability(self,player:"Player",opponent:"Player",selected_object:tuple["Card"]):
        func,card=await self.undo_stack(player,opponent)
        cost=sum(card.cost.values())
        await self.attact_to_object(card.player,cost,"rgba(255,215,0,0.9)","Missile_Hit")
        