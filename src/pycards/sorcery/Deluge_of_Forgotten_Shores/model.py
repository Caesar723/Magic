from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Deluge_of_Forgotten_Shores(Sorcery):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":3}

        self.fixed_id:int=268

        self.name:str="Deluge of Forgotten Shores"
        self.type:str="Sorcery"
        self.mana_cost:str="6UUU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Return all creatures your opponent controls to their owners' hands. Draw {draw_count_word} card{draw_count_plural}."
        self.image_path:str="cards/sorcery/Deluge of Forgotten Shores/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            for creature in list(opponent.battlefield):
                owner=creature.player
                owner.remove_card(creature,"battlefield")
                owner.append_card(creature.copy_for_player(owner),"hand")
            player.draw_card(self.effect_params["draw_count"])
        finally:
            player.action_store.end_record()
