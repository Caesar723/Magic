
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure
from initinal_file import CARD_DICTION



class Boots_of_Blinding_Speed(Treasure):
    name="Boots of Blinding Speed"
    content="At the start of your game, add 2 Islands to your land area."
    price=12
    background="Crafted by a mischievous gnome who loved to outpace his enemies."
    image_path="treasures/Boots_of_Blinding_Speed/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.game_start
        async def game_start(self_player):
            result=await previews_func()
            player.action_store.start_record()
            player.append_card(CARD_DICTION["Island_Land"](player),"land_area")
            player.append_card(CARD_DICTION["Island_Land"](player),"land_area")
            player.action_store.end_record()
            return result
        player.game_start = types.MethodType(game_start, player)

