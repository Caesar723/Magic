
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Temporal_Distortion(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"extra_turns":1}

        self.name:str="Temporal Distortion"

        self.type:str="Sorcery"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Temporal Distortion allows you to take {extra_turns_article_an} extra turn{extra_turns_plural} after this one. Exile Temporal Distortion."
        self.image_path:str="cards/sorcery/Temporal Distortion/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        player.add_counter_dict("extra_turn",self.effect_params["extra_turns"])
        self.flag_dict["exile"]=True

