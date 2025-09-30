
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.treasure import Treasure
from game.buffs import StateBuff
import random
from game.type_cards.creature import Creature


class Shield_of_the_Trickster_Buff(StateBuff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        
        power,live=  selected_card.state
        power_,live_=int(live-power),int(power-live)
        super().__init__(card,selected_card,power_,live_)
        self.buff_name=f"{card.name}"
        self.content="swap the Attack and Health of a random enemy minion."
        self.color_missile="rgba(203, 203, 203, 0.9)"
        self.buff_missile="Missile_Hit"

        

class Shield_of_the_Trickster(Treasure):
    name="Shield of the Trickster"
    content="At the start of your turn, swap the Attack and Health of a random enemy minion."
    price=8
    background="Crafted by mischievous fae, this shield confounds foes with its unpredictable magic."
    image_path="treasures/Shield_of_the_Trickster/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.beginning_phase
        async def beginning_phase(self_player):
            result=await previews_func()
            
            cards=player.opponent.get_cards_by_pos_type("battlefield",(Creature,))
            if cards:
                card=random.choice(cards)
                buff=Shield_of_the_Trickster_Buff(self,card)
                card.gain_buff(buff,card)
            return result
        player.beginning_phase = types.MethodType(beginning_phase, player)
