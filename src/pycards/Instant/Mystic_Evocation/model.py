
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object


class Mystic_Evocation(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=38

        self.name:str="Mystic Evocation"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target noncreature spell. If that spell is countered this way, scry 2."
        self.image_path:str="cards/Instant/Mystic Evocation/image.jpg"

        self.undo_range="Sorcery|Instant|Land"


    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        func,card = await self.undo_stack(player,opponent)
        
        await self.Scry(player,opponent,2)