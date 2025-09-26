
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Lucky_Charm_of_the_Mischievous_Sprite(Treasure):
    name="Lucky Charm of the Mischievous Sprite"
    content="At the start of your turn, add a random beneficial effect to your hand."
    price=0
    background="Crafted by mischievous sprites, this charm brings luck to those who bear it."
    image_path="treasures/Lucky_Charm_of_the_Mischievous_Sprite/image.png"

    def change_function(self,player:"Player"):
        pass
