
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Mirror_of_Reflection(Treasure):
    name="Mirror of Reflection"
    content="Whenever your opponent plays a minion, summon a 1/1 copy of it on your side of the board."
    price=0
    background="A mystical mirror that mirrors the actions of one's foes, turning their own minions against them."
    image_path="treasures/Mirror_of_Reflection/image.png"

    def change_function(self,player:"Player"):
        pass
