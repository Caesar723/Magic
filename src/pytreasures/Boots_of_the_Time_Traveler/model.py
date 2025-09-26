
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Boots_of_the_Time_Traveler(Treasure):
    name="Boots of the Time Traveler"
    content="At the start of your turn, you may change the turn number to any number between 1 and 10."
    price=0
    background="Crafted by a legendary gnome inventor, these boots allow the wearer to manipulate time itself."
    image_path="treasures/Boots_of_the_Time_Traveler/image.png"

    def change_function(self,player:"Player"):
        pass
