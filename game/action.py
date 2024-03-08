

from game.card import Card


class Action:

    def __init__(self,card_hold:Card,show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.card_hold:Card=card_hold # store the controled card

    def __repr__(self) -> str:
        pass