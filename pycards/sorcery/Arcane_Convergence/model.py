
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Arcane_Convergence(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Arcane Convergence"

        self.type:str="Sorcery"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Arcane Convergence allows you to untap all lands you control and add X mana in any combination of colors to your mana pool, where X is the number of sorcery cards in your graveyard."
        self.image_path:str="cards/sorcery/Arcane Convergence/image.jpg"



        