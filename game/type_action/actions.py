

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.card import Card
    from game.player import Player

from game.action import Action



class Creature_Start_Attack(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player",attack_obj:"Card|Player",show_hide:bool,state_self:tuple,state_attacted:tuple) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.attack_obj:"Card|Player"=attack_obj # store the selected_object card
        self.state_self:tuple=state_self
        self.state_attacted:tuple=state_attacted
    
    def text(self,player)-> str:
        pass

class Creature_Prepare_Attack(Action):
    pass

class Creature_Prepare_Defense(Action):
    pass


class Activate_Ability(Action):
    pass

class Select_Object(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card


class Add_Buff(Select_Object):
    pass


class Attack_To_Object(Select_Object):#这种伤害自己的随从是不会受伤的
    pass

class Cure_To_Object(Select_Object):
    pass

class Gain_Card(Select_Object):
    pass

class Lose_Card(Select_Object):
    pass

class Die(Action):
    pass


class Summon(Action):
    pass

class Turn(Action):# your turn!
    pass

class Change_Mana(Action):
    pass