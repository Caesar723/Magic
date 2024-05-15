

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.card import Card
    from game.player import Player

#from game.action import Action




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
        self.list_action:list[Action]=list_action

    def text(self,player):
        action_text=[action.text(player) for action in self.list_action]
        return f"action_list({",".join(action_text)})"
    




class Creature_Start_Attack(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player",attack_obj:"Card|Player",show_hide:bool,state_self:tuple,state_attacted:tuple) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.attack_obj:"Card|Player"=attack_obj # store the selected_object card
        self.state_self:tuple=state_self
        self.state_attacted:tuple=state_attacted
    
    def text(self,player)-> str:
        state_self=f"state({",".join(map(str,self.state_self))})"
        state_attacted=f"state({",".join(map(str,self.state_attacted))})"
        return f"action(Creature_Start_Attack,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.attack_obj.text(player)},{state_self},{state_attacted}))"

class Creature_Prepare_Attack(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
       
    def text(self,player)-> str:
        
        return f"action(Creature_Prepare_Attack,parameters({self.object_hold.text(player)},{self.player.text(player)}))"

class Play_Cards(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player",deleted_card:"Card") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.deleted_card:"Card"=deleted_card
       
    def text(self,player)-> str:
        
        return f"action(Play_Cards,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.object_hold.text(player)},showOBJ()))"


class Creature_Prepare_Defense(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player",attack_obj:"Card|Player",show_hide:bool):
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.attack_obj:"Card|Player"=attack_obj # store the selected_object card

    def text(self,player)-> str:
        
        return f"action(Creature_Prepare_Defense,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.attack_obj.text(player)}))"
class Activate_Ability(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
       
    def text(self,player)-> str:
        
        return f"action(Activate_Ability,parameters({self.object_hold.text(player)},{self.player.text(player)}))"

class Reset_Ability(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
       
    def text(self,player)-> str:
        
        return f"action(Reset_Ability,parameters({self.object_hold.text(player)},{self.player.text(player)}))"
    
class Select_Object(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card


class Add_Buff(Select_Object):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",final_state:tuple,show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        self.final_state:tuple=final_state
    def text(self,player)-> str:
        final_state=f"state({",".join(map(str,self.final_state))})"
        
        return f"action(Add_Buff,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.object_selected.text(player)},{final_state}))"
    


class Attack_To_Object(Select_Object):#这种伤害自己的随从是不会受伤的
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",color:str,type:str,final_state:tuple) -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        self.color=color
        self.type=type
        self.final_state=final_state
    def text(self,player)-> str:
        final_state=f"state({",".join(map(str,self.final_state))})"
        
        return f"action(Attack_To_Object,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.object_selected.text(player)},{self.color},{self.type},{final_state}))"
    

class Cure_To_Object(Select_Object):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",color:str,type:str,final_state:tuple) -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        self.color=color
        self.type=type
        self.final_state=final_state
    def text(self,player)-> str:
        final_state=f"state({",".join(map(str,self.final_state))})"
        
        return f"action(Cure_To_Object,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.object_selected.text(player)},{self.color},{self.type},{final_state}))"
    

class Gain_Card(Select_Object):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        
    def text(self,player)-> str:
        
        return f"action(Gain_Card,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.object_selected.text(player)}))"
    

class Lose_Card(Select_Object):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        
    def text(self,player)-> str:
        
        return f"action(Lose_Card,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.object_selected.text(player)}))"
    

class Die(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
       
    def text(self,player)-> str:
        
        return f"action(Die,parameters({self.object_hold.text(player)},{self.player.text(player)}))"



class Summon(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
       
    def text(self,player)-> str:
        
        return f"action(Summon,parameters({self.object_hold.text(player)},{self.player.text(player)}))"


class Turn(Action):# your turn!
    def __init__(self,object_hold:"Card|Player",player:"Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
       
    def text(self,player)-> str:
        
        return f"action(Turn,parameters({self.object_hold.text(player)},{self.player.text(player)}))"


class Change_Mana(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player",mana:list) -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.mana=mana

    def text(self,player)-> str:
        mana=f"state({",".join(map(str,self.mana))})" 
        return f"action(Turn,parameters({self.object_hold.text(player)},{self.player.text(player)},{mana}))"







