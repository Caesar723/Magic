
from hmac import new
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.type_cards.creature import Creature
from game.treasure import Treasure



class Mirror_of_Reflection(Treasure):
    name="Mirror of Reflection"
    content="Whenever your opponent plays a minion, summon a 1/1 copy of it on your side of the board."
    price=32
    background="A mystical mirror that mirrors the actions of one's foes, turning their own minions against them."
    image_path="treasures/Mirror_of_Reflection/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.opponent.play_a_card
        async def play_a_card(self_player,card):
            result=await previews_func(card)
            if result[0] and result[1]!="cancel":
                if isinstance(card,Creature):
                    new_card=type(card)(player)
                    new_card.live=1
                    new_card.power=1
                    new_card.actual_live=1
                    new_card.actual_power=1
                    player.action_store.start_record()
                    player.append_card(new_card,"battlefield")
                    player.action_store.end_record()
            return result
        player.opponent.play_a_card = types.MethodType(play_a_card, player.opponent)
