
from __future__ import annotations
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import KeyBuff,Buff
from game.type_cards.creature import Creature
from game.game_function_tool import select_object,send_select_request


class Mystic_Barrier_Buff(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.buff_name=f"{card.name}"
        self.content="Can't cast noncreature spells until end of turn."
        
        self.card_type:str="Control"

    def change_function(self,card):
        previews_func=card.check_can_use

        def check_can_use(self_card,player):
            result=previews_func(player)
            if isinstance(card,Creature):
                return result
            else:
                return (False,"Can't cast noncreature spells until end of turn.")
        card.check_can_use = types.MethodType(check_can_use, card)

class Mystic_Barrier(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=34

        self.name:str="Mystic Barrier"

        self.type:str="Instant"

        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Choose one - your creatures gain hexproof until end of turn.Target player can't cast noncreature spells until end of turn."
        self.image_path:str="cards/Instant/Mystic Barrier/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        if selected_object:
            if selected_object[0].selection_index==1:
                for card in player.battlefield:
                    buff=KeyBuff(self,card,"Hexproof")
                    card.gain_buff(buff,self)
                
                
            elif selected_object[0].selection_index==2:

                for card in opponent.hand:
                    buff=Mystic_Barrier_Buff(self,card)
                    card.gain_buff(buff,self)
                

        
    async def selection_step(self, player: "Player" = None, opponent: "Player" = None,selection_random:bool=False):
        selection1=self.create_selection("your creatures gain hexproof until end of turn",1)
        selection2=self.create_selection("target player can't cast noncreature spells until end of turn",2)
        card=await player.send_selection_cards([selection1,selection2],selection_random)
        print(card)
        
        return [card]