
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Ephemeral_Vision(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":1,"scry_count":2}

        self.name:str="Ephemeral Vision"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Draw {draw_count_article} card{draw_count_plural}. Scry {scry_count}."
        self.image_path:str="cards/Instant/Ephemeral Vision/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        player.draw_card(self.effect_params["draw_count"])
        await self.Scry(player,opponent,self.effect_params["scry_count"])

