
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Mindful_Reflection(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":2,"discard_count":1}

        self.name:str="Mindful Reflection"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Draw {draw_count_word} card{draw_count_plural}, then discard {discard_count_article} card{discard_count_plural}."
        self.image_path:str="cards/sorcery/Mindful Reflection/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        player.draw_card(self.effect_params["draw_count"])
        for _ in range(self.effect_params["discard_count"]):
            if player.hand:
                card=await player.send_selection_cards(player.hand,selection_random=True)
                if card!="cancel":
                    player.discard(card)

