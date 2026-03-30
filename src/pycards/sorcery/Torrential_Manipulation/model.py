
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_cards.instant import Instant
from game.type_cards.instant import Instant_Undo
import random


class Torrential_Manipulation(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=236

        self.name:str="Torrential Manipulation"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Return target creature to its owner's hand. You randomly cast an instant or sorcery spell without paying its mana cost."
        self.image_path:str="cards/sorcery/Torrential Manipulation/image.jpg"

    @select_object("opponent_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            target = selected_object[0]
            if target in opponent.battlefield:
                opponent.remove_card(target, "battlefield")
                opponent.append_card(type(target)(opponent), "hand")
        sorceries = opponent.get_cards_by_pos_type("hand", (Sorcery,Instant),except_type=(Instant_Undo,))
        if sorceries:
            sorcery = random.choice(sorceries)
            await player.auto_play_card(sorcery,start_bullet_time=False)




        