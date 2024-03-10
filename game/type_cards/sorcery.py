from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player





from game.card import Card



class Sorcery(Card):
    
    def __init__(self) -> None:
        super().__init__()

    def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):# when player use the card
        pass

    def calculate_spell_power(self):
        pass

    def when_select_target(self):
        pass

    def when_play_this_card(self,
                            player:'Player'=None,
                            opponent:'Player'=None,
                            ):# when player use the card
        self.card_ability(self,player,opponent)
    