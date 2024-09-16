
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import StateBuff,Indestructible

class Honorable_Protection(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Honorable Protection"

        self.type:str="Instant"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Target creature you control gains indestructible until end of turn. If it's a Knight, put a +1/+1 counter on it."
        self.image_path:str="cards/Instant/Honorable Protection/image.jpg"


    @select_object("all_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            buff_i=Indestructible(self,selected_object[0])
            buff_i.set_end_of_turn()
            selected_object[0].gain_buff(buff_i,self)
            if "Knight" in selected_object[0].type_card:
                buff=StateBuff(self,selected_object[0],1,1)
                selected_object[0].gain_buff(buff,self)