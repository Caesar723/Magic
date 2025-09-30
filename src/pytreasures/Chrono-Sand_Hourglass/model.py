
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class Chrono_Sand_Hourglass(Treasure):
    name="Chrono-Sand Hourglass"
    content="At the start of your turn, replay your last played card for free."
    price=40
    background="Crafted by ancient time mages to bend the rules of time."
    image_path="treasures/Chrono-Sand_Hourglass/image.png"

    def change_function(self,player:"Player"):
        
        previews_func_beginning_phase=player.beginning_phase
        previews_func_playcard=player.play_a_card

        card_record=None


        async def beginning_phase(self_player):
            result=await previews_func_beginning_phase()
            nonlocal card_record
            if card_record:
                new_card=type(card_record)(player)
                await player.auto_play_card(new_card)
            card_record=None
            
            return result

        async def play_a_card(self_player,card):
            nonlocal card_record
            result=await previews_func_playcard(card)
            if result[0]:
                card_record=card
            return result

        player.beginning_phase = types.MethodType(beginning_phase, player)
        player.play_a_card = types.MethodType(play_a_card, player)