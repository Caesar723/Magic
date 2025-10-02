
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player


from game.treasure import Treasure
from game.buffs import KeyBuff
from game.type_cards.creature import Creature

class Cloak_of_the_Shadow_Thief(Treasure):
    name="Cloak of the Shadow Thief"
    content="Your creatures gain lifelink."
    price=25
    background="Woven from shadows stolen from the realm of stealthy assassins, this cloak grants its wearer the ability to vanish from sight."
    image_path="treasures/Cloak_of_the_Shadow_Thief/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.append_card
        def append_card(self_player,card,type):
            result=previews_func(card,type)
            if isinstance(card,Creature) and type=="battlefield":
                buff=KeyBuff(self,card,"lifelink")
                
                card.gain_buff(buff,card)
                
            return result
        player.append_card = types.MethodType(append_card, player)
