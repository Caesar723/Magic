
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure
from initinal_file import CARD_DICTION


class Boots_of_the_Swift_Strider(Treasure):
    name="Boots of the Swift Strider"
    content="At the start of your game, add 1 Forests to your land area."
    price=18
    background="Crafted by elusive forest creatures to enhance speed and agility."
    image_path="treasures/Boots_of_the_Swift_Strider/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.game_start
        async def game_start(self_player):
            result=await previews_func()
            player.action_store.start_record()
            player.append_card(CARD_DICTION["Forest_Land"](player),"land_area")
            player.action_store.end_record()
            return result
        player.game_start = types.MethodType(game_start, player)

