
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import Clone
import random


class Mystic_Reflection(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=40

        self.name:str="Mystic Reflection"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Choose target creature. If another creature with the same name is on the battlefield, transform that creature into a copy of the chosen creature until end of turn."
        self.image_path:str="cards/Instant/Mystic Reflection/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if not selected_object:
            return
        source = selected_object[0]
        all_creatures = list(player.battlefield) + list(opponent.battlefield)
        candidates = [c for c in all_creatures if c is not source and getattr(c, "name", "") == source.name]
        if not candidates:
            return
        target = random.choice(candidates)
        buff = Clone(self, source, target)
        buff.set_end_of_turn()
        target.gain_buff(buff, self)