
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import StateBuff, KeyBuff


class Swift_Ward(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=68

        self.name:str="Swift Ward"

        self.type:str="Instant"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Target creature gets +1/+1 until end of turn and gains hexproof until end of turn."
        self.image_path:str="cards/Instant/Swift Ward/image.jpg"

    @select_object("your_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        if not selected_object:
            return
        target=selected_object[0]
        buff=StateBuff(self,target,1,1)
        buff.set_end_of_turn()
        target.gain_buff(buff,self)
        hexproof=KeyBuff(self,target,"Hexproof")
        hexproof.set_end_of_turn()
        target.gain_buff(hexproof,self)

