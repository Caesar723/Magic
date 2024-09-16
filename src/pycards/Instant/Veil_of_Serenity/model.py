
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Veil_of_Serenity(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Veil of Serenity"

        self.type:str="Instant"

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Exile target enchantment or creature spell."
        self.image_path:str="cards/Instant/Veil of Serenity/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self, player: 'Player' = None, opponent: 'Player' = None, selected_object: tuple['Card'] = ...):
        if selected_object:
            await self.exile_object(selected_object[0],"rgba(255,255,0,0.7)","Missile_Hit")
            
        