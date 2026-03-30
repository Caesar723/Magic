
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant_Undo
from game.game_function_tool import select_object
import random


class Mystic_Tide(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystic Tide"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell unless its controller's mana pool is less than 3. If you control an Island, you may return random opponent's creature to its owner's hand."
        self.image_path:str="cards/Instant/Mystic Tide/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        stack = player.room.stack
        if not stack:
            return
        _func, card = stack[-1]
        if card.player != opponent or card.type == "Land":
            return
        if not opponent.check_can_use({"colorless":3,"U":0,"W":0,"B":0,"R":0,"G":0})[0]:
            await self.undo_stack(player, opponent)
            has_island = any(getattr(land, "name", "") == "Island" for land in player.land_area)
            if has_island and opponent.battlefield:
                creature = random.choice(opponent.battlefield)
                opponent.remove_card(creature, "battlefield")
                opponent.append_card(type(creature)(opponent), "hand")




        