
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.instant import Instant


class Mystic_Reflection(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Reflection"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Choose target creature. If another creature with the same name is on the battlefield, transform that creature into a copy of the chosen creature until end of turn."
        self.image_path:str="cards/Instant/Mystic Reflection/image.jpg"

    def card_ability(self, player: Player = None, opponent: Player = None, selected_object: tuple[Card] = ...):
        super().card_ability(player, opponent, selected_object)
        print("Mystic_Reflection")

        