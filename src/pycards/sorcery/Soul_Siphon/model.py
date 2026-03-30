
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random


class Soul_Siphon(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=228

        self.name:str="Soul Siphon"

        self.type:str="Sorcery"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Randomly destroy an opponent's creature. You gain life equal to that creature's power."
        self.image_path:str="cards/sorcery/Soul Siphon/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        if not opponent.battlefield:
            return
        creature=random.choice(opponent.battlefield)
        gain=creature.state[0]
        await self.destroy_object(creature,"rgba(0,0,0,0.5)","Cure")
        await self.cure_to_object(player,gain,"rgba(0,255,0,1)","Cure")

        

