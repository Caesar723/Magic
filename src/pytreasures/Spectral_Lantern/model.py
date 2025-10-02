
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure
from game.buffs import StateBuff
import random
from game.type_cards.creature import Creature



class Spectral_Lantern(Treasure):
    name="Spectral Lantern"
    content="Whenever you gain life, put a +1/+1 counter on target creature you control."
    price=17
    background="A lantern that illuminates the battlefield with ghostly light."
    image_path="treasures/Spectral_Lantern/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.when_gaining_life
        async def when_gaining_life(self_player,card,value):
            result=await previews_func(card,value)
            
            creatures=player.get_cards_by_pos_type("battlefield",(Creature,))
            if creatures:
                creature=random.choice(creatures)

                buff=StateBuff(self,creature,1,1)
                player.action_store.start_record()
                creature.gain_buff(buff,creature)
                player.action_store.end_record()
            return result
        player.when_gaining_life = types.MethodType(when_gaining_life, player)
