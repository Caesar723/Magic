
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Chrono_Sand_Hourglass(Treasure):
    name="Chrono-Sand Hourglass"
    content="At the start of your turn, replay your last played card for free."
    price=0
    background="Crafted by ancient time mages to bend the rules of time."
    image_path="treasures/Chrono-Sand_Hourglass/image.png"

    def change_function(self,player:"Player"):
        pass
