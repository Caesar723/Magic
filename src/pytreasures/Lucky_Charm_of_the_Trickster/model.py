
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Lucky_Charm_of_the_Trickster(Treasure):
    name="Lucky Charm of the Trickster"
    content="At the start of your turn, flip a coin. If heads, gain +1 Mana Crystal this turn."
    price=0
    background="Crafted by a mischievous goblin, this charm brings luck to those who dare to take risks."
    image_path="treasures/Lucky_Charm_of_the_Trickster/image.png"

    def change_function(self,player:"Player"):
        pass
