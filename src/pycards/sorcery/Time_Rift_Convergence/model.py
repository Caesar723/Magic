
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random


class Time_Rift_Convergence(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Time Rift Convergence"

        self.type:str="Sorcery"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Return up to two target cards from your graveyard to your hand."
        self.image_path:str="cards/sorcery/Time Rift Convergence/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        cards=random.sample(player.graveyard,2)
        for card in cards:
            player.remove_card(card,"graveyard")
            player.append_card(type(card)(player),"hand")
        

