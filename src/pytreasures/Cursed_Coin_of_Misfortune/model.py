
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure
from game.type_action import actions
import random

class Cursed_Coin_of_Misfortune(Treasure):
    name="Cursed Coin of Misfortune"
    content="At the start of each turn, flip a coin - heads, gain 2 green mana crystals; tails, discard a random card."
    price=6
    background="This cursed coin brings luck and misfortune in equal measure, tempting adventurers with its unpredictable rewards."
    image_path="treasures/Cursed_Coin_of_Misfortune/image.png"

    def change_function(self,player:"Player"):

        previews_func=player.beginning_phase
        async def beginning_phase(self_player):
            result=await previews_func()
            if random.randint(0,1)==0:
                player.mana["G"]+=2
                player.action_store.add_action(actions.Change_Mana(player,player,player.get_manas()))
            elif player.hand:
                random_card=random.choice(player.hand)
                player.discard(random_card)
            return result
        player.beginning_phase = types.MethodType(beginning_phase, player)
