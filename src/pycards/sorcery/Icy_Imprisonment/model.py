
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import Frozen

class Icy_Imprisonment(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Icy Imprisonment"

        self.type:str="Sorcery"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Freeze all creatures your opponents control until the start of your next turn."
        self.image_path:str="cards/sorcery/Icy Imprisonment/image.jpg"


    @select_object("",1)
    async def card_ability(self,player: "Player",opponent: "Player",selected_object:tuple["Card"]):
        for creature in opponent.battlefield:
            buff=Frozen(self,creature)
            creature.gain_buff(buff,self)

