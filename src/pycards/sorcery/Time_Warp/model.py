
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random

class Time_Warp(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Time Warp"

        self.type:str="Sorcery"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Draw two cards, then randomly discard a card. You may put a card from your graveyard on top of your library."
        self.image_path:str="cards/sorcery/Time Warp/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        player.draw_card(2)
        if player.hand:
            card=random.choice(player.hand)
            player.discard(card)
        cards=random.sample(player.graveyard,1)
        if cards:
            card=cards[0]
            player.remove_card(card,"graveyard")
            player.library.insert(0,type(card)(player))


        