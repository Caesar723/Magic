
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Apocalypse_Riders(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Apocalypse Riders"

        self.type:str="Sorcery"

        self.mana_cost:str="5WW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Summon four 2/2 Knight creature tokens, each with a different ability (Trample, Haste, Lifelink, Flying)."
        self.image_path:str="cards/sorcery/Apocalypse Riders/image.jpg"



        