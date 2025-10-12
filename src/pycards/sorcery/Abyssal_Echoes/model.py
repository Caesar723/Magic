
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_cards.creature import Creature
import random
class Abyssal_Echoes(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Abyssal Echoes"

        self.type:str="Sorcery"

        self.mana_cost:str="5BB"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Search your library for a creature card with a mana value of 7 or greater and put it onto the battlefield."
        self.image_path:str="cards/sorcery/Abyssal Echoes/image.jpg"

    @select_object("",1)
    async def card_ability(self,player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        cards_library=player.get_cards_by_pos_type("library",(Creature))
        cards_library=[
            card for card in cards_library 
            if card.cost["colorless"]+card.cost["B"]+card.cost["R"]+card.cost["G"]+card.cost["U"]+card.cost["W"]>=7
        ]
        if cards_library:
            card_library:"Creature"=random.choice(cards_library)

            # player.action_store.start_record()
            await player.auto_play_card(card_library,start_bullet_time=False)
        