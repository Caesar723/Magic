
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import StateBuff, KeyBuff


class Overgrowth_Surge(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=50

        self.name:str="Overgrowth Surge"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Target creature gets +3/+3 until end of turn. If that creature is a Treefolk, it also gains trample until end of turn."
        self.image_path:str="cards/Instant/Overgrowth Surge/image.jpg"

    @select_object("your_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        if not selected_object:
            return
        target=selected_object[0]
        state_buff=StateBuff(self,target,3,3)
        state_buff.set_end_of_turn()
        target.gain_buff(state_buff,self)
        if "Treefolk" in getattr(target,"type_card","") or "Treefolk" in getattr(target,"type_creature",""):
            key_buff=KeyBuff(self,target,"Trample")
            key_buff.set_end_of_turn()
            target.gain_buff(key_buff,self)

