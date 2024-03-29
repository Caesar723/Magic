
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Mystic_Convergence(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystic Convergence"

        self.type:str="Instant"

        self.mana_cost:str="2GW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Prevent all combat damage that would be dealt this turn. At the beginning of your next main phase, add X mana in any combination of colors to your mana pool, where X is the amount of combat damage prevented this way."
        self.image_path:str="cards/Instant/Mystic Convergence/image.jpg"



        