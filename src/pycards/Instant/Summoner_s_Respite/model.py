
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Summoner_s_Respite(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=66

        self.name:str="Summoner's Respite"

        self.type:str="Instant"

        self.mana_cost:str="3GW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Prevent all combat damage that would be dealt this turn. You gain 4 life. Put a +1/+1 counter on each creature you control."
        self.image_path:str="cards/Instant/Summoner's Respite/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.buffs import StateBuff
        
        await player.gains_life(self,4)
        
        for creature in player.battlefield:
            buff = StateBuff(self, creature, 1, 1)
            creature.gain_buff(buff, self)




        