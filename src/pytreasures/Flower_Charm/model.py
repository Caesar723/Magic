
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure
from game.buffs import StateBuff
import random
from game.type_cards.creature import Creature
from game.type_action import actions


class Flower_Charm(Treasure):
    name="Flower Charm"
    content="At the start of your turn, restore 5 HP."
    price=40
    background="A radiant relic. Permanently reduce all incoming damage by half."
    image_path="treasures/Flower_Charm/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.beginning_phase
        async def beginning_phase(self_player):
            player.action_store.start_record()
            result=await previews_func()
            await player.gains_life(self,5)
            player.action_store.add_action(actions.Cure_To_Object(player,player,player,"rgba(103, 203, 103, 0.9)","Cure",[player.life]))
            await player.check_dead()   
            player.action_store.end_record()
            return result
        player.beginning_phase = types.MethodType(beginning_phase, player)
