
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Cloak_of_the_Shadow_Thief(Treasure):
    name="Cloak of the Shadow Thief"
    content="After your hero attacks, Stealth for the rest of the turn."
    price=0
    background="Woven from shadows stolen from the realm of stealthy assassins, this cloak grants its wearer the ability to vanish from sight."
    image_path="treasures/Cloak_of_the_Shadow_Thief/image.png"

    def change_function(self,player:"Player"):
        pass
