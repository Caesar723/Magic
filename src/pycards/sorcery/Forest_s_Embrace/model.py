
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains
from pycards.land.Swamp.model import Swamp
from pycards.land.Mountain.model import Mountain
from pycards.land.Island.model import Island
import random


class Forest_s_Embrace(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Forest's Embrace"

        self.type:str="Sorcery"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Search your library for up to three land cards, put them onto the battlefield tapped, then shuffle your library."
        self.image_path:str="cards/sorcery/Forest's Embrace/image.jpg"


    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):

        for i in range(3):
            lands=player.get_cards_by_pos_type("library",(Forest,Plains,Swamp,Mountain,Island))
            if lands:
                random_land=random.choice(lands)
                player.append_card(random_land,"land_area")
                player.remove_card(random_land,"library")
                random_land.tap()
        random.shuffle(player.library)

        