
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Naturalize(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Naturalize"

        self.type:str="Sorcery"

        self.mana_cost:str="3G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Destroy target creature."
        self.image_path:str="cards/sorcery/Naturalize/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        if not selected_object:
            return
        target=selected_object[0]
        
        await self.destroy_object(target,"rgba(144, 238, 144, 0.8)","Missile_Hit")
        

