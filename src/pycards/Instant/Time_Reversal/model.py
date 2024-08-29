
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object
from game.type_cards.sorcery import Sorcery

class Time_Reversal(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Time Reversal"

        self.type:str="Instant"

        self.mana_cost:str="5UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Undo all spells and effects from your opponent."
        self.image_path:str="cards/Instant/Time Reversal/image.jpg"

        self.undo_range="Sorcery|Instant"

    
    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        async def empty_func():pass
        for i in range(len(self.stack)):
            if self.stack[i][1].player==opponent and \
            (isinstance(self.stack[i][1],Sorcery) or isinstance(self.stack[i][1],Instant)):
                self.stack[i]=(empty_func,self.stack[i][1])




