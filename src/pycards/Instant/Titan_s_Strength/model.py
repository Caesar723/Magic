
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import StateBuff,KeyBuff


class Titan_s_Strength(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Titan's Strength"

        self.type:str="Instant"

        self.mana_cost:str="2GG"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until end of turn, your creatures get +4/+4 and Trample."
        self.image_path:str="cards/Instant/Titan's Strength/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        for creature in player.battlefield:
            buff_state=StateBuff(self,creature,4,4)
            buff_state.set_end_of_turn()
            creature.gain_buff(buff_state,self)

            buff_key=KeyBuff(self,creature,"Trample")
            buff_key.set_end_of_turn()
            creature.gain_buff(buff_key,self)

        return await super().card_ability(player, opponent, selected_object)
        