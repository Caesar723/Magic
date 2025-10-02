
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure
from game.buffs import StateBuff
import random
from game.type_cards.creature import Creature



class Sun_Ring(Treasure):
    name="Sun Ring"
    content="Permanently reduce all incoming damage by half."
    price=40
    background="A radiant relic. Permanently reduce all incoming damage by half."
    image_path="treasures/Sun_Ring/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.take_damage
        async def take_damage(self_player,card,value):
            value=max(value-1,0)
            result=await previews_func(card,value)
            return result
        player.take_damage = types.MethodType(take_damage, player)
