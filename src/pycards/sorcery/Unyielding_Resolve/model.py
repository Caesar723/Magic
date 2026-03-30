
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import KeyBuff, Indestructible


class Unyielding_Resolve(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=240

        self.name:str="Unyielding Resolve"

        self.type:str="Sorcery"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Unyielding Resolve gives all creatures you control indestructible until end of turn. Creatures you control gain lifelink until end of turn."
        self.image_path:str="cards/sorcery/Unyielding Resolve/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        for creature in list(player.battlefield):
            ind=Indestructible(self,creature)
            ind.set_end_of_turn()
            creature.gain_buff(ind,self)
            life=KeyBuff(self,creature,"lifelink")
            life.set_end_of_turn()
            creature.gain_buff(life,self)

