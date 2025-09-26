
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Shield_of_the_Trickster(Treasure):
    name="Shield of the Trickster"
    content="At the start of your turn, swap the Attack and Health of a random enemy minion."
    price=0
    background="Crafted by mischievous fae, this shield confounds foes with its unpredictable magic."
    image_path="treasures/Shield_of_the_Trickster/image.png"

    def change_function(self,player:"Player"):
        pass
