
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import Tap

class Temporal_Flux(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Temporal Flux"

        self.type:str="Sorcery"

        self.mana_cost:str="4U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Tap all creatures your opponents control. They don't untap during their next untap step."
        self.image_path:str="cards/sorcery/Temporal Flux/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        for creature in opponent.battlefield:
            buff=Tap(self,creature)
            creature.gain_buff(buff,self)
        


        