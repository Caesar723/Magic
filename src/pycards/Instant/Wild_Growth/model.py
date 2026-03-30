
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains
from pycards.land.Swamp.model import Swamp
from pycards.land.Mountain.model import Mountain
from pycards.land.Island.model import Island
import random


class Wild_Growth(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Wild Growth"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Search your library for a basic land card and put it onto the battlefield tapped, then shuffle your library."
        self.image_path:str="cards/Instant/Wild Growth/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        basic_lands=player.get_cards_by_pos_type("library",(Plains,Swamp,Mountain,Island,Forest))
        if basic_lands:
            land=random.choice(basic_lands)
            player.remove_card(land,"library")
            player.append_card(land,"land_area")
            land.tap()
            random.shuffle(player.library)

