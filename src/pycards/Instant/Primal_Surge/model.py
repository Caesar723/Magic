
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Primal_Surge(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Primal Surge"

        self.type:str="Instant"

        self.mana_cost:str="2G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Target player shuffles their hand and graveyard into their library, then draws that many cards. They may play an additional land this turn."
        self.image_path:str="cards/Instant/Primal Surge/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        for card_hand in list(player.hand):
            player.remove_card(card_hand,"hand")
            player.append_card(card_hand,"library")

            player.draw_card(1)

        player.add_counter_dict("lands_summon_max",1)
        self.flag_dict["return land max"]=True

    async def when_end_turn(self,player: "Player" = None, opponent: "Player" = None):#OK
        if self.get_flag("return land max"):
            player.add_counter_dict("lands_summon_max",-1)
        self.flag_dict["return land max"]=False
        