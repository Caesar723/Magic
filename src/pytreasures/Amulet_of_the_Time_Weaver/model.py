
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Amulet_of_the_Time_Weaver(Treasure):
    name="Amulet of the Time Weaver"
    content="When it's the 5th turn, you can have an additional turn."
    price=20
    background="An enchanted amulet created by a mystical time-warping mage, allowing the wearer to rewind time and alter their actions."
    image_path="treasures/Amulet_of_the_Time_Weaver/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.beginning_phase

        async def beginning_phase(self_player):
            result=await previews_func()
            if player.get_counter_from_dict("turn_count")==5:
                player.add_counter_dict("extra_turn",1)
            return result
            
            
        
        player.beginning_phase = types.MethodType(beginning_phase, player)
