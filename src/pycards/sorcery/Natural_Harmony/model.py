
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


class Natural_Harmony(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Natural Harmony"

        self.type:str="Sorcery"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Search your library for a basic land card and put it onto the battlefield tapped, then shuffle your library. You gain 2 life."
        self.image_path:str="cards/sorcery/Natural Harmony/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        cards=player.get_cards_by_pos_type("library",(Forest,Plains,Swamp,Mountain,Island))
        if cards:
            card=random.choice(cards)
            player.remove_card(card,"library")
            player.append_card(card,"land_area")
            card.tap()
        await self.cure_to_object(player, 2, "rgba(0,255,0,1)", "Cure")

