
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Verdant_Harvest(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Verdant Harvest"

        self.type:str="Sorcery"

        self.mana_cost:str="1GG"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Search your library for a basic land card and put it onto the battlefield tapped, then shuffle your library. Draw a card."
        self.image_path:str="cards/sorcery/Verdant Harvest/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from pycards.land.Forest.model import Forest
        from pycards.land.Plains.model import Plains
        from pycards.land.Island.model import Island
        from pycards.land.Mountain.model import Mountain
        from pycards.land.Swamp.model import Swamp
        
        lands = player.get_cards_by_pos_type("library", (Forest, Plains, Island, Mountain, Swamp))
        if lands:
            land = await player.send_selection_cards(lands, selection_random=True)
            player.remove_card(land, "library")
            player.append_card(land, "land_area")
            land.tap()
            player.draw_card(1)




        