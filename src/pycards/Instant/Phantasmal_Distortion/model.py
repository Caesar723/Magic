
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import Clone
import random

class Phantasmal_Distortion(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=52

        self.name:str="Phantasmal Distortion"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until end of turn, target creature you control becomes a copy of another your random creature, except it retains its abilities. Return that creature to its owner's hand at the beginning of the next end step."
        self.image_path:str="cards/Instant/Phantasmal Distortion/image.jpg"

    @select_object("your_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        
        if selected_object and player.battlefield:
            target = random.choice([card for card in player.battlefield if card is not selected_object[0]])
            source = selected_object[0]
            buff = Clone(self, source,target)
            buff.set_end_of_turn()
            source.gain_buff(buff, self)




        