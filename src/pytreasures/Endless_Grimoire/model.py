from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player


from game.type_cards.sorcery import Sorcery
from game.type_cards.instant import Instant
from game.treasure import Treasure



class Endless_Grimoire(Treasure):
    name="Endless Grimoire"
    content="Whenever you cast a sorcery or instant, draw a card."
    price=16
    background="A spellbook that never runs out."
    image_path="treasures/Endless_Grimoire/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.play_a_card
        async def play_a_card(self_player,card):
            result=await previews_func(card)
            if result[0]:
                if isinstance(card,Sorcery) or isinstance(card,Instant):
                    player.draw_card(1)
            return result
            
        player.play_a_card = types.MethodType(play_a_card, player)