
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Boots_of_the_Swift_Strider(Treasure):
    name="Boots of the Swift Strider"
    content="At the start of your turn, gain +1 Mana Crystal this turn only."
    price=0
    background="Crafted by elusive forest creatures to enhance speed and agility."
    image_path="treasures/Boots_of_the_Swift_Strider/image.png"

    def change_function(self,player:"Player"):
        pass
