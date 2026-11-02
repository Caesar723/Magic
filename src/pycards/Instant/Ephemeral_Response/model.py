
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant_Undo
from game.game_function_tool import select_object


class Ephemeral_Response(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"scry_count":1,"mana_threshold":2}

        self.name:str="Ephemeral Response"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Counter target spell unless its controller pays {mana_threshold}. If it is countered this way, scry {scry_count}."
        self.image_path:str="cards/Instant/Ephemeral Response/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        stack=player.room.stack
        if not stack:
            return
        card=stack[-1]["card"]
        if card.player!=opponent or card.type=="Land":
            return
        total_mana=sum(opponent.mana.values())
        if total_mana<self.effect_params["mana_threshold"]:
            await self.undo_stack(player, opponent)
            await self.Scry(player,opponent,self.effect_params["scry_count"])

