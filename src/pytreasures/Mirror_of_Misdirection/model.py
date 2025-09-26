
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Mirror_of_Misdirection(Treasure):
    name="Mirror of Misdirection"
    content="Whenever your opponent targets a friendly minion with a spell or effect, redirect it to a different target of your choice."
    price=0
    background="Crafted by mischievous gnomes, this enchanted mirror confounds even the most skilled spellcasters."
    image_path="treasures/Mirror_of_Misdirection/image.png"

    def change_function(self,player:"Player"):
        pass
