
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant_Undo
from game.game_function_tool import select_object


class Ethereal_Surge(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ethereal Surge"

        self.type:str="Instant"

        self.mana_cost:str="UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. If that spell is countered this way, return it to its owner's hand instead of putting it into their graveyard."
        self.image_path:str="cards/Instant/Ethereal Surge/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        func, card = await self.undo_stack(player, opponent)
        card.player.remove_card(card,"graveyard")
        card.player.append_card(type(card)(card.player),"hand")




        