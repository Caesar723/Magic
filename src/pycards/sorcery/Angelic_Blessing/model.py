
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 

from game.type_cards.creature import Creature
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff,KeyBuff

class Angelic_Blessing(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Angelic Blessing"

        self.type:str="Sorcery"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Target creature gets +3/+3 and gains vigilance until end of turn."
        self.image_path:str="cards/sorcery/Angelic Blessing/image.jpg"

    
    @select_object("all_creatures",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        if selected_object:
            target_card=selected_object[0]
            buff=StateBuff(self,selected_object[0],3,3)
            buff.set_end_of_turn()
            target_card.gain_buff(buff,self)
            buff=KeyBuff(self,target_card,"Vigilance")
            buff.set_end_of_turn()
            target_card.gain_buff(buff,self)