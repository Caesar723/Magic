
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import StateBuff,KeyBuff

class Verdant_Growth(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Verdant Growth"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Target creature gets +4/+4 until end of turn. If it's a Treefolk creature, it gains trample until end of turn."
        self.image_path:str="cards/Instant/Verdant Growth/image.jpg"
    @select_object("all_creatures",1)
    async def card_ability(self, player: 'Player' = None, opponent: 'Player' = None, selected_object: tuple['Card'] = ...):
        if selected_object:
            buff_state=StateBuff(self,selected_object[0],4,4)
            buff_state.set_end_of_turn()
            selected_object[0].gain_buff(buff_state,self)
            
            if "Treefolk" in selected_object[0].type_card:
                buff_key=KeyBuff(self,selected_object[0],"Trample")
                buff_key.set_end_of_turn()
                selected_object[0].gain_buff(buff_key,self)
            


        