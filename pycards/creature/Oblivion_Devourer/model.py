
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature


class Oblivion_Devourer(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Oblivion Devourer"
        self.live:int=6
        self.power:int=6

        self.type_creature:str="Eldrazi Creature - Eldrazi"
        self.type:str="Creature"

        self.mana_cost:str="5BB"
        self.color:str="black"
        self.type_card:str="Eldrazi Creature - Eldrazi"
        self.rarity:str="Rare"
        self.content:str="Menace (This creature can't be blocked except by two or more creatures), When Oblivion Devourer attacks, you may sacrifice another creature. If you do, target player discards two cards."
        self.image_path:str="cards/creature/Oblivion Devourer/image.jpg"



        