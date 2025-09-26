
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Amulet_of_the_Time_Weaver(Treasure):
    name="Amulet of the Time Weaver"
    content="Once per game, replay your last turn."
    price=0
    background="An enchanted amulet created by a mystical time-warping mage, allowing the wearer to rewind time and alter their actions."
    image_path="treasures/Amulet_of_the_Time_Weaver/image.png"

    def change_function(self,player:"Player"):
        pass
