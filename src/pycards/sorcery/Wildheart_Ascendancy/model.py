from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff, KeyBuff


class Wildheart_Ascendancy(Sorcery):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"power_bonus":3,"toughness_bonus":3}

        self.fixed_id:int=254

        self.name:str="Wildheart Ascendancy"
        self.type:str="Sorcery"
        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Creatures you control get +{power_bonus}/+{toughness_bonus} and gain trample until end of turn."
        self.image_path:str="cards/sorcery/Wildheart Ascendancy/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            for creature in list(player.battlefield):
                state=StateBuff(self,creature,self.effect_params["power_bonus"],self.effect_params["toughness_bonus"])
                state.set_end_of_turn()
                creature.gain_buff(state,self)
                trample=KeyBuff(self,creature,"Trample")
                trample.set_end_of_turn()
                creature.gain_buff(trample,self)
        finally:
            player.action_store.end_record()
