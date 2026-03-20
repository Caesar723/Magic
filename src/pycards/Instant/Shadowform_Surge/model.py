
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Shadowform_Surge(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=63

        self.name:str="Shadowform Surge"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Target creature gets -3/-3 until end of turn. If that creature dies this turn, create a 2/2 black Shade creature token with lifelink."
        self.image_path:str="cards/Instant/Shadowform Surge/image.jpg"

    @select_object("opponent_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.buffs import StateBuff
        
        if selected_object:
            target = selected_object[0]
            buff = StateBuff(self, target, -3, -3)
            buff.set_end_of_turn()
            target.gain_buff(buff, self)




        