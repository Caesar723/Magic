
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object


class Warlock_s_Dark_Pact(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Warlock's Dark Pact"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. Its controller loses life equal to its mana cost."
        self.image_path:str="cards/Instant/Warlock's Dark Pact/image.jpg"



    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        func,card = await self.undo_stack(player,opponent)
        cost=sum(card.cost.values())
        await self.attact_to_object(card.player,cost,"rgba(0,0,0,0.9)","Missile_Hit")
        
        