from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player


from game.type_cards.sorcery import Sorcery
from game.type_cards.instant import Instant
from game.type_cards.creature import Creature
from game.treasure import Treasure



class Different_Creature_Creature(Creature):
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Different Creature"
        self.live:int=1
        self.power:int=1
        self.actual_live:int=1
        self.actual_power:int=1
        self.type_creature:str="Creature"
        self.type:str="Creature"

        self.mana_cost:str="1"
        self.color:str="green"
        self.type_card:str="Creature"
        self.rarity:str="Rare"
        self.content:str="Generate random number of creatures."
        self.image_path:str="cards/creature/Ancient Stonewood/image.jpg"


class Different_Creature(Treasure):
    name="Different Creature"
    content="Generate random number of creatures."
    price=1
    background="A spellbook that never runs out."
    image_path="treasures/Endless_Grimoire/image.png"

    def change_function(self,player:"Player"):
        pass