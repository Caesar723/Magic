
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Vorinclex__Apex_of_Mutation(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Vorinclex, Apex of Mutation"
        self.live:int=6
        self.power:int=6
        self.actual_live:int=6
        self.actual_power:int=6

        self.type_creature:str="Legendary Creature - Phyrexian Mutant"
        self.type:str="Creature"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Legendary Creature - Phyrexian Mutant"
        self.rarity:str="Mythic Rare"
        self.content:str="Trample, Infect, and whenever you cast a spell, proliferate. Whenever an opponent proliferates, they must pay 2 life for each permanent type they've chose (Artifact, creature, enchantment, land, planeswalker, or any combination thereof)."
        self.image_path:str="cards/creature/Vorinclex, Apex of Mutation/image.jpg"



        