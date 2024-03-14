
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature


class Igni_the_Pyromancer(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Igni the Pyromancer"
        self.live:int=2
        self.power:int=2

        self.type_creature:str="Human Shaman"
        self.type:str="Creature"

        self.mana_cost:str="2R"
        self.color:str="red"
        self.type_card:str="Human Shaman"
        self.rarity:str="Rare"
        self.content:str="Whenever Igni the Pyromancer deals damage to a player, you may cast an instant or sorcery spell from your graveyard without paying its mana cost."
        self.image_path:str="cards/creature/Igni the Pyromancer/image.jpg"



        