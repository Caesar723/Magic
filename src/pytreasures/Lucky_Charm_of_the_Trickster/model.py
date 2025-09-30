
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure
import random
from game.type_action import actions


class Lucky_Charm_of_the_Trickster(Treasure):
    name="Lucky Charm of the Trickster"
    content="At the start of your turn, flip a coin. If heads, gain +1 Mana Crystal this turn."
    price=7
    background="Crafted by a mischievous goblin, this charm brings luck to those who dare to take risks."
    image_path="treasures/Lucky_Charm_of_the_Trickster/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.beginning_phase
        async def beginning_phase(self_player):
            result=await previews_func()
            if random.randint(0,1)==0:
                player.mana["W"]+=1
                player.action_store.add_action(actions.Change_Mana(player,player,player.get_manas()))
            return result
        player.beginning_phase = types.MethodType(beginning_phase, player)
