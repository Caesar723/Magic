
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Torrent_Elemental(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Torrent Elemental"
        self.live:int=3
        self.power:int=2
        self.actual_live:int=3
        self.actual_power:int=2

        self.type_creature:str="Elemental"
        self.type:str="Creature"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Elemental"
        self.rarity:str="Uncommon"
        self.content:str="Flash (You may cast this spell any time you could cast an instant) and Flying"
        self.image_path:str="cards/creature/Torrent Elemental/image.jpg"



        