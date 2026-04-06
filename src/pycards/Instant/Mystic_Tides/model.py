
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant_Undo
from game.game_function_tool import select_object
from game.buffs import Tap
import random


class Mystic_Tides(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystic Tides"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Counter target spell unless its controller's mana pool is less than 2. If it is countered this way, tap random opponent's creature."
        self.image_path:str="cards/Instant/Mystic Tides/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        func,card=await self.undo_stack(player,opponent)
        buff_tap=Tap(self,random.choice(opponent.battlefield))
        random.choice(opponent.battlefield).gain_buff(buff_tap,self)



    def check_can_use(self, player: 'Player') -> tuple[bool]:
        result,reason=super().check_can_use(player)
        if not result:
            return (result,reason)
        if self.player.room.get_cost_total(player)<2:
            return (False,"not enough mana")
        else:
            return (True,"")


