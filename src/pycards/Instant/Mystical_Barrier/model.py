
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object


class Mystical_Barrier(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=45

        self.name:str="Mystical Barrier"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target spell. If Mystical Barrier is countered this way, you may draw a card."
        self.image_path:str="cards/Instant/Mystical Barrier/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        func,card=await self.undo_stack(player,opponent)
        
        player.draw_card(1)

        