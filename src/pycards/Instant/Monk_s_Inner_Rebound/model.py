
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object
from game.type_cards.sorcery import Sorcery

class Monk_s_Inner_Rebound(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Monk's Inner Rebound"

        self.type:str="Instant"

        self.mana_cost:str="1WWW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter a spell. Redirect its effects back to random object."
        self.image_path:str="cards/Instant/Monk's Inner Rebound/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        func,card=await self.undo_stack(player,opponent)
        if (isinstance(card,Instant) and not isinstance(card,Instant_Undo)) or isinstance(card,Sorcery):
            new_card=type(card)(player)
            new_func=await new_card.card_ability(player,opponent,auto_select=True)
            self.stack.append((new_func,new_card))
        
        
        





        