
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff


class Harvest_Blessing(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Harvest Blessing"

        self.type:str="Sorcery"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Search your library for a basic land card, put it onto the battlefield tapped, then shuffle your library. Target creature you control gets +1/+1 until end of turn."
        self.image_path:str="cards/sorcery/Harvest Blessing/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        for card in list(player.library):
            if getattr(card,"type","")=="Land":
                player.remove_card(card,"library")
                player.append_card(card,"land_area")
                card.tap()
                break
        if selected_object:
            buff=StateBuff(self,selected_object[0],1,1)
            buff.set_end_of_turn()
            selected_object[0].gain_buff(buff,self)

