
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random

class Mystic_Reversal(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystic Reversal"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Each player draws a card, then discards a card."
        self.image_path:str="cards/sorcery/Mystic Reversal/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        player.draw_card(1)
        opponent.draw_card(1)
        if player.hand:
            player.discard(random.choice(player.hand))
        if opponent.hand:
            opponent.discard(random.choice(opponent.hand))
        




        