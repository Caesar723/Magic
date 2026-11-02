
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
        self.effect_params:dict={"draw_count":1,"discard_count":1}

        self.name:str="Mystic Reversal"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Each player draws {draw_count_article} card{draw_count_plural}, then discards {discard_count_article} card{discard_count_plural}."
        self.image_path:str="cards/sorcery/Mystic Reversal/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        player.draw_card(self.effect_params["draw_count"])
        opponent.draw_card(self.effect_params["draw_count"])
        for _ in range(self.effect_params["discard_count"]):
            if player.hand:
                player.discard(random.choice(player.hand))
        for _ in range(self.effect_params["discard_count"]):
            if opponent.hand:
                opponent.discard(random.choice(opponent.hand))
        




        