
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 

from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Ephemeral_Insight(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ephemeral Insight"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Scry 2, then draw a card. Put this card to your hand again."
        self.image_path:str="cards/Instant/Ephemeral Insight/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
       await self.Scry(player,opponent,2)
       player.draw_card(1)

       if not self.get_flag("been used"):
           new_card=type(self)(player)
           new_card.flag_dict["been used"]=True
           player.action_store.start_record()
           player.append_card(new_card,"hand")
           player.action_store.end_record()
        