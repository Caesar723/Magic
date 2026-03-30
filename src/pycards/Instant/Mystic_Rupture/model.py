
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Mystic_Rupture(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=42

        self.name:str="Mystic Rupture"

        self.type:str="Instant"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Return all nonland permanents to their owner's hands. Each player may search their library for a basic land card, put it onto the battlefield tapped, then shuffle their library."
        self.image_path:str="cards/Instant/Mystic Rupture/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        all_permanents = list(player.battlefield) + list(opponent.battlefield) + list(player.land_area) + list(opponent.land_area)
        for perm in all_permanents:
            if not hasattr(perm, 'type') or perm.type != "Land":
                owner = perm.player
                if perm in owner.battlefield:
                    owner.remove_card(perm, "battlefield")
                    owner.append_card(type(perm)(owner), "hand")




        