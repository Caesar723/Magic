
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Boots_of_the_Time_Traveler(Treasure):
    name="Boots of the Time Traveler"
    content="At the beginning of your upkeep, you may put a time counter on Boots of the Time Traveler. Then, if there are exactly 10 time counters on it, take an extra turn after this one and set the time counter to 0."
    price=23
    background="Crafted by a legendary gnome inventor, these boots allow the wearer to manipulate time itself."
    image_path="treasures/Boots_of_the_Time_Traveler/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.upkeep_step
        async def upkeep_step(self_player):
            player.add_counter_dict("time_counter_Boots_of_the_Time_Traveler",1)
            if player.get_counter_from_dict("time_counter_Boots_of_the_Time_Traveler")==10:
                player.add_counter_dict("extra_turn",1)
                player.set_counter_dict("time_counter_Boots_of_the_Time_Traveler",0)
            result=await previews_func()
            
            return result
        player.upkeep_step = types.MethodType(upkeep_step, player)
