
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Overgrowth(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Overgrowth"

        self.type:str="Sorcery"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Search your library for a basic land card and put it onto the battlefield tapped. Then shuffle your library. Untap up to one land you control."
        self.image_path:str="cards/sorcery/Overgrowth/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        for card in list(player.library):
            if getattr(card,"type","")=="Land":
                player.remove_card(card,"library")
                player.append_card(card,"land_area")
                card.tap()
                break
        for land in player.land_area:
            if land.get_flag("tap"):
                land.untap()
                break

