
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant_Undo
from game.game_function_tool import select_object


class Mystical_Shift(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystical Shift"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Counter target spell and draw a card unless its controller's mana pool is less than 3."
        self.image_path:str="cards/Instant/Mystical Shift/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        stack=player.room.stack
        if stack:
            _func,card=stack[-1]
            if card.player==opponent and card.type!="Land":
                if not opponent.check_can_use({"colorless":3,"U":0,"W":0,"B":0,"R":0,"G":0})[0]:
                    await self.undo_stack(player, opponent)
                    player.draw_card(1)

