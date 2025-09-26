
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Spectral_Lantern(Treasure):
    name="Spectral Lantern"
    content="Your Hero Power can target minions."
    price=0
    background="A lantern that illuminates the battlefield with ghostly light."
    image_path="treasures/Spectral_Lantern/image.png"

    def change_function(self,player:"Player"):
        pass
