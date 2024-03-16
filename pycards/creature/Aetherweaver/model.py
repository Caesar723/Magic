
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Aetherweaver(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Aetherweaver"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Wizard"
        self.type:str="Creature"

        self.mana_cost:str="3U"
        self.color:str="blue"
        self.type_card:str="Human Wizard"
        self.rarity:str="Mythic Rare"
        self.content:str="When Aetherweaver enters the battlefield, you may return target artifact or enchantment from your graveyard to your hand."
        self.image_path:str="cards/creature/Aetherweaver/image.jpg"



        