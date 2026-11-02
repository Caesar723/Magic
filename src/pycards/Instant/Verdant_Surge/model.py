
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import StateBuff,KeyBuff


class Verdant_Surge(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"power_bonus":2,"toughness_bonus":4}

        self.fixed_id:int=82

        self.name:str="Verdant Surge"

        self.type:str="Instant"

        self.mana_cost:str="1GG"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Target creature you control gets +{power_bonus}/+{toughness_bonus} until end of turn. If that creature is a Druid, it also gains reach until end of turn."
        self.image_path:str="cards/Instant/Verdant Surge/image.jpg"



    @select_object("all_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            creature=selected_object[0]
            buff=StateBuff(self,creature,self.effect_params["power_bonus"],self.effect_params["toughness_bonus"])
            buff.set_end_of_turn()
            creature.gain_buff(buff,self)
            if creature.type_creature=="Druid":
                buff=KeyBuff(self,creature,"reach")
                buff.set_end_of_turn()
                creature.gain_buff(buff,self)