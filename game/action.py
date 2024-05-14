
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.card import Card
    from game.player import Player


class Action:

    def __init__(self,object_hold:"Card|Player",player:"Player",show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card

    def text(self,player)-> str:
        pass

    def __repr__(self) -> str:
        pass

class List_Action_Genarator:
    pass

class List_Action:
    def __init__(self,list_action) -> None:
        pass