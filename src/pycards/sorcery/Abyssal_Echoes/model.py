
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
        self.effect_params:dict={"mana_threshold":7}

        self.fixed_id:int=180

        self.name:str="Abyssal Echoes"

        self.type:str="Sorcery"

        self.mana_cost:str="5BB"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Search your library for a creature card with a mana value of {mana_threshold} or greater and put it onto the battlefield."
        self.image_path:str="cards/sorcery/Abyssal Echoes/image.jpg"

    @select_object("",1)
    async def card_ability(self,player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        cards_library=player.get_cards_by_pos_type("library",(Creature))
        cards_library=[
            card for card in cards_library 
            if card.cost["colorless"]+card.cost["B"]+card.cost["R"]+card.cost["G"]+card.cost["U"]+card.cost["W"]>=self.effect_params["mana_threshold"]
        ]
        if cards_library:
            card_library:"Creature"=random.choice(cards_library)
            library_index=player.library.index(card_library)
            listeners=[key for key in card_library.check_overwritten() if card_library in player.get_cards_from_dict(key)]
            player.remove_card(card_library,"library")
            success,_=await player.auto_play_card(card_library,start_bullet_time=False)
            if not success:
                player.library.insert(library_index,card_library)
                for key in listeners:
                    player.put_card_to_dict(key,card_library)
        