
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Boots_of_Blazing_Speed(Treasure):
    name="Boots of Blazing Speed"
    content="At the start of your turn, gain +2 Mana Crystals this turn only."
    price=0
    background="Crafted by ancient fire elementals, these boots grant incredible swiftness to their wearer."
    image_path="treasures/Boots_of_Blazing_Speed/image.png"

    def change_function(self,player:"Player"):
        pass
