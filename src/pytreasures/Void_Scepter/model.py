
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure
from game.buffs import StateBuff
import random
from game.type_cards.creature import Creature
from game.type_action import actions



class Void_Scepter(Treasure):
    name="Void Scepter"
    content="At the first beginning phase of the game, deal 10 preemptive damage to opponent."
    price=40
    background="A radiant relic. At the first beginning phase of the game, deal 10 preemptive damage to opponent."
    image_path="treasures/Void_Scepter/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.beginning_phase
        flag=False
        async def beginning_phase(self_player):
            nonlocal flag
            result=await previews_func()

            if flag:
                
                return result

            player.action_store.start_record()
            await player.opponent.take_damage(self,10)
            player.action_store.add_action(actions.Attack_To_Object(player,player,player.opponent,"rgba(103, 103, 203, 0.9)","Cure",[player.opponent.life]))
            await player.opponent.check_dead()
            player.action_store.end_record()
            flag=True
            return result
        player.beginning_phase = types.MethodType(beginning_phase, player)
