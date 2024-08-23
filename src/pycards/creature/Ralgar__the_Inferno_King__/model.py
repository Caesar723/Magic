
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Ralgar__the_Inferno_King__(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ralgar, the Inferno King  "
        self.live:int=4
        self.power:int=5
        self.actual_live:int=4
        self.actual_power:int=5

        self.type_creature:str="Elemental Creature  "
        self.type:str="Creature"

        self.mana_cost:str="3RR  "
        self.color:str="colorless"
        self.type_card:str="Elemental Creature  "
        self.rarity:str="Mythic Rare  "
        self.content:str="When Ralgar enters the battlefield, it deals 3 damage to any target. Whenever you cast an instant or sorcery spell, Ralgar gets +1/+0 until end of turn.  "
        self.image_path:str="cards/creature/Ralgar, the Inferno King  /image.jpg"



        