
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
import random
from game.buffs import Frozen,StateBuff


class Temporal_Shift(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Temporal Shift"

        self.type:str="Instant"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Randomly freeze up to two enemy creatures and halve their health.Add a time counter. When it reaches 10, take an extra turn."
        self.image_path:str="cards/Instant/Temporal Shift/image.jpg"


    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if opponent.battlefield:
            if len(opponent.battlefield)>=2:
                creatures=random.sample(opponent.battlefield,2)
            else:
                creatures=opponent.battlefield[0:1]
        
            for creature in creatures:
                buff=StateBuff(self,creature,0,-creature.state[1]//2)
                
                buff_frozen=Frozen(self,creature)
                creature.gain_buff(buff,self)
                creature.gain_buff(buff_frozen,self)
                
        player.add_time_counter(1)
        