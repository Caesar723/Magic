
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff,KeyBuff


class Righteous_Conviction(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"power_bonus":2,"toughness_bonus":2}

        self.fixed_id:int=227

        self.name:str="Righteous Conviction"

        self.type:str="Sorcery"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Choose a creature you control. Until end of turn, that creature gets +{power_bonus}/+{toughness_bonus} and gains lifelink."
        self.image_path:str="cards/sorcery/Righteous Conviction/image.jpg"


    @select_object("your_creatures",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        if selected_object:
            buff=StateBuff(self,selected_object[0],self.effect_params["power_bonus"],self.effect_params["toughness_bonus"])
            buff.set_end_of_turn()
            selected_object[0].gain_buff(buff,self)
            buff=KeyBuff(self,selected_object[0],"lifelink")
            buff.set_end_of_turn()
            selected_object[0].gain_buff(buff,self)
        