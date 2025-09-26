
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Lucky_Clover_Pin(Treasure):
    name="Lucky Clover Pin"
    content="At the start of your turn, add a random Lucky Charm card to your hand."
    price=0
    background="A small, enchanted pin that brings luck and charms to those who wear it."
    image_path="treasures/Lucky_Clover_Pin/image.png"

    def change_function(self,player:"Player"):
        pass
