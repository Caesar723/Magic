
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Cursed_Coin_of_Misfortune(Treasure):
    name="Cursed Coin of Misfortune"
    content="At the start of each turn, flip a coin - heads, gain 2 mana crystals; tails, discard a random card."
    price=0
    background="This cursed coin brings luck and misfortune in equal measure, tempting adventurers with its unpredictable rewards."
    image_path="treasures/Cursed_Coin_of_Misfortune/image.png"

    def change_function(self,player:"Player"):
        pass
