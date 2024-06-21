
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Fiery_Blast(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Fiery Blast"

        self.type:str="Instant"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Fiery Blast deals 2 damage to any target."
        self.image_path:str="cards/Instant/Fiery Blast/image.jpg"

    @select_object("all_roles",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        if selected_object:

            player.action_store.start_record()
            await self.attact_to_object(selected_object[0],2,"rgba(243, 0, 0, 0.9)","Missile_Hit")
            player.action_store.end_record()


        