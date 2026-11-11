from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import Clone


class Mystic_Reflection(Instant):
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={}
        self.fixed_id:int=40
        self.name:str="Mystic Reflection"
        self.type:str="Instant"
        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Target creature becomes a copy of a creature on either battlefield with the greatest combined current power and toughness until the end of its controller's turn. If tied, choose one at random."
        self.image_path:str="cards/Instant/Mystic Reflection/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        if not selected_object:
            return
        target=selected_object[0]
        creatures=[card for card in player.battlefield+opponent.battlefield
                   if not card.get_flag("die") and not card.get_flag("exile") and card.state[1]>0]
        if target not in creatures:
            return
        largest=max(sum(card.state) for card in creatures)
        reference=random.choice([card for card in creatures if sum(card.state)==largest])
        if reference is target:
            return
        buff=Clone(self,target,reference)
        buff.set_end_of_turn()
        target.gain_buff(buff,self)
