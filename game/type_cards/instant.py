from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player




from game.card import Card
from game.type_action import actions




class Instant(Card):
    
    def __init__(self) -> None:
        super().__init__()

    def card_ability(self):
        pass

    def calculate_spell_power(self):
        pass

    def when_select_target(self):
        pass

    def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):# when player use the card
        super().when_play_this_card(player, opponent)

        player.remove_card(self,"hand")

        self.card_ability()
