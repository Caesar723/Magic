
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff,KeyBuff


class Righteous_Conviction(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Righteous Conviction"

        self.type:str="Sorcery"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Choose a creature you control. Until end of turn, that creature gets +2/+2 and gains lifelink."
        self.image_path:str="cards/sorcery/Righteous Conviction/image.jpg"


    @select_object("your_creatures",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        if selected_object:
            buff=StateBuff(self,selected_object[0],2,2)
            buff.set_end_of_turn()
            selected_object[0].gain_buff(buff,self)
            buff=KeyBuff(self,selected_object[0],"lifelink")
            buff.set_end_of_turn()
            selected_object[0].gain_buff(buff,self)
        