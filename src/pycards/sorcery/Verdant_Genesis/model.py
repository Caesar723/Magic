
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff


class Verdant_Genesis(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Verdant Genesis"

        self.type:str="Sorcery"

        self.mana_cost:str="5G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Search your library for up to two land cards, put them onto the battlefield tapped, then shuffle your library. You may put a +1/+1 counter on each creature you control."
        self.image_path:str="cards/sorcery/Verdant Genesis/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        count=0
        for card in list(player.library):
            if getattr(card,"type","")=="Land":
                player.remove_card(card,"library")
                player.append_card(card,"land_area")
                card.tap()
                count+=1
                if count>=2:
                    break
        for creature in list(player.battlefield):
            creature.gain_buff(StateBuff(self,creature,1,1),self)

