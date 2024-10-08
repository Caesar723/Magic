
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff

class Natural_Growth(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Natural Growth"

        self.type:str="Sorcery"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Target creature gets +2/+2 until end of turn."
        self.image_path:str="cards/sorcery/Natural Growth/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):# when player use the card
        if selected_object:
            buff=StateBuff(self,selected_object[0],2,2)
            buff.set_end_of_turn()
            selected_object[0].gain_buff(buff,self)



        