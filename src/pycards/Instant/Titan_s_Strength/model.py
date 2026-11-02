
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
        self.effect_params:dict={"power_bonus":4,"toughness_bonus":4}

        self.fixed_id:int=75

        self.name:str="Titan's Strength"

        self.type:str="Instant"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until end of turn, your creatures get +{power_bonus}/+{toughness_bonus} and Trample."
        self.image_path:str="cards/Instant/Titan's Strength/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        for creature in player.battlefield:
            buff_state=StateBuff(self,creature,self.effect_params["power_bonus"],self.effect_params["toughness_bonus"])
            buff_state.set_end_of_turn()
            creature.gain_buff(buff_state,self)

            buff_key=KeyBuff(self,creature,"Trample")
            buff_key.set_end_of_turn()
            creature.gain_buff(buff_key,self)

        return await super().card_ability(player, opponent, selected_object)
        