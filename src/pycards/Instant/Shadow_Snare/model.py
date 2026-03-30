
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import StateBuff


class Shadow_Snare(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=62

        self.name:str="Shadow Snare"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Target creature gets -3/-3 until end of turn."
        self.image_path:str="cards/Instant/Shadow Snare/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            target = selected_object[0]
            debuff = StateBuff(self, target, -3, -3)
            debuff.set_end_of_turn()
            target.gain_buff(debuff, self)


        