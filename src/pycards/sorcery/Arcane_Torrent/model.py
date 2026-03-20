
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Arcane_Torrent(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=184

        self.name:str="Arcane Torrent"

        self.type:str="Sorcery"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Arcane Torrent allows you to search your library for a sorcery card, reveal it, and put it into your hand. Then shuffle your library."
        self.image_path:str="cards/sorcery/Arcane Torrent/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.type_cards.sorcery import Sorcery
        
        sorceries = player.get_cards_by_pos_type("library", (Sorcery,))
        if sorceries:
            sorcery = await player.send_selection_cards(sorceries, selection_random=True)
            player.remove_card(sorcery, "library")
            player.append_card(sorcery, "hand")




        