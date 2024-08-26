
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Temporal_Traveler(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Temporal Traveler"
        self.live:int=4
        self.power:int=3
        self.actual_live:int=4
        self.actual_power:int=3

        self.type_creature:str="Creature - Wizard"
        self.type:str="Creature"

        self.mana_cost:str="4UU"
        self.color:str="blue"
        self.type_card:str="Creature - Wizard"
        self.rarity:str="Rare"
        self.content:str="Whenever Temporal Traveler attacks, you may cast an instant or sorcery card from your graveyard without paying its mana cost."
        self.image_path:str="cards/creature/Temporal Traveler/image.jpg"



        