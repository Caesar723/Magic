
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Awaken_the_Elemental(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Awaken the Elemental"

        self.type:str="Sorcery"

        self.mana_cost:str="4GG"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Return a creature card from your graveyard to the battlefield, then put five +1/+1 counters on it until end of turn."
        self.image_path:str="cards/sorcery/Awaken the Elemental/image.jpg"



        