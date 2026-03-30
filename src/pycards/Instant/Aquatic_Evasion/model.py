
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import KeyBuff


class Aquatic_Evasion(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Aquatic Evasion"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Target creature you control gains hexproof until end of turn. Draw a card."
        self.image_path:str="cards/Instant/Aquatic Evasion/image.jpg"

    @select_object("your_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        player.draw_card(1)
        if not selected_object:
            return
        target=selected_object[0]
        buff=KeyBuff(self,target,"Hexproof")
        buff.set_end_of_turn()
        target.gain_buff(buff,self)
        

