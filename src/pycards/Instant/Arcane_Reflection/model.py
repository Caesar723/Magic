
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
import random


class Arcane_Reflection(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=6

        self.name:str="Arcane Reflection"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Arcane Reflection allows return random instant or sorcery card from your graveyard to your hand."
        self.image_path:str="cards/Instant/Arcane Reflection/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.type_cards.instant import Instant
        from game.type_cards.sorcery import Sorcery
        
        cards = [
            c
            for c in player.get_cards_by_pos_type("graveyard", (Instant, Sorcery))
            if c is not self
        ]
        if cards:
            card = random.choice(cards)
            player.remove_card(card, "graveyard")
            player.append_card(type(card)(player), "hand")




        