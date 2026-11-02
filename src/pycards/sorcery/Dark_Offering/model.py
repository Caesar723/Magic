
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Dark_Offering(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"heal":2,"life_loss":2}

        self.fixed_id:int=196

        self.name:str="Dark Offering"

        self.type:str="Sorcery"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Opponent player loses {life_loss} life and you gain {heal} life."
        self.image_path:str="cards/sorcery/Dark Offering/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        await self.attact_to_object(opponent, self.effect_params["life_loss"], "rgba(80,0,120,1)", "Missile_Hit")
        await self.cure_to_object(player, self.effect_params["heal"], "rgba(0,255,0,1)", "Cure")

