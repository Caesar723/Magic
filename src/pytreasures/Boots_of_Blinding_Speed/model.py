
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Boots_of_Blinding_Speed(Treasure):
    name="Boots of Blinding Speed"
    content="At the start of your turn, gain +2 Mana Crystals this turn only."
    price=0
    background="Crafted by a mischievous gnome who loved to outpace his enemies."
    image_path="treasures/Boots_of_Blinding_Speed/image.png"

    def change_function(self,player:"Player"):
        pass
