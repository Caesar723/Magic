
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff, KeyBuff


class Divine_Blessing(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Divine Blessing"

        self.type:str="Sorcery"

        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Target creature gets +2/+2 and lifelink until end of turn."
        self.image_path:str="cards/sorcery/Divine Blessing/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        if not selected_object:
            return
        target=selected_object[0]
        state=StateBuff(self,target,2,2)
        state.set_end_of_turn()
        target.gain_buff(state,self)
        lifelink=KeyBuff(self,target,"lifelink")
        lifelink.set_end_of_turn()
        target.gain_buff(lifelink,self)



        