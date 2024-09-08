
from __future__ import annotations
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import Buff
from game.type_cards.creature import Creature


class Phantom_Shield_Buff(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card
        self.card_type:str="Prevent all damage"
        self.content:str="Prevent all damage that would be dealt to this creature this turn."
        self.buff_name=f"{card.name}"
    
    def change_function(self,card:"Creature"):
        previews_func=card.take_damage
        async def take_damage(self_card,card,value,player, opponent):# 可以受到来自各种卡牌的伤害
            result=await previews_func(card,0,player,opponent)
            return result
        card.take_damage = types.MethodType(take_damage, card)


class Phantom_Shield(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Phantom Shield"

        self.type:str="Instant"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until end of turn, your creatures gain 'Prevent all damage that would be dealt to this creature this turn.'"
        self.image_path:str="cards/Instant/Phantom Shield/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        for creature in player.battlefield:
            buff=Phantom_Shield_Buff(self,creature)
            buff.set_end_of_turn()
            creature.gain_buff(buff,self)
        return await super().card_ability(player, opponent, selected_object)
        