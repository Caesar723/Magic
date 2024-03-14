
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature


class Spectral_Harbinger(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Spectral Harbinger"
        self.live:int=3
        self.power:int=2

        self.type_creature:str="Spirit Creature - Spirit"
        self.type:str="Creature"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Spirit Creature - Spirit"
        self.rarity:str="Rare"
        self.content:str="Flying, Lifelink (Damage dealt by this creature also causes you to gain that much life), When Spectral Harbinger enters the battlefield, you may exile target creature card from a graveyard. If you do, you gain 2 life."
        self.image_path:str="cards/creature/Spectral Harbinger/image.jpg"



        