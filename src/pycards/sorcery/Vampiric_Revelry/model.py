
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random

class Vampiric_Revelry(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=241

        self.name:str="Vampiric Revelry"

        self.type:str="Sorcery"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="randomly destroy an creature. You gain life equal to that creature's toughness."
        self.image_path:str="cards/sorcery/Vampiric Revelry/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        creature=random.choice(opponent.battlefield+player.battlefield)
        gain=creature.state[1]
        await self.destroy_object(creature,"rgba(0,0,0,0.5)","Cure")
        await self.cure_to_object(player, max(gain, 0), "rgba(0,255,0,1)", "Cure")

