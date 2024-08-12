from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.card import Card
    from game.player import Player
    from game.buffs import Buff
import asyncio
#from game.action import Action




class Action:

    def __init__(self,object_hold:"Card|Player",player:"Player",show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card

    def check_inhand(self,obj:"Card|Player",player):
        if (obj in self.player.opponent.hand or obj in self.player.hand):
            select_text=obj.text(player,self.show_hide)
        else:
            select_text=obj.text(player)
        return select_text
    
    def text(self,player)-> str:
        pass


    def __repr__(self) -> str:
        return self.__class__.__name__

class List_Action_Processor:
    def __init__(self,cache,cache_condition) -> None:
        self.action_list:list[list]=[]
        self.start_counter=-1
        self.action_cache:list=cache
        self.action_condition=cache_condition


    def start_record(self):#在start期间没有end又start，会把action list分开，像括号一样(abc(abcde)de)
        self.action_list.append([])
        self.start_counter+=1


    def end_record(self):#pack the actions

        self.start_counter-=1
        if self.start_counter==-1:
            for arr in self.action_list:
                if arr:
                    self.action_cache.append(List_Action(arr))
                    
                    asyncio.create_task(self.notify_condition())
                    
                    # except RuntimeError as e:
                    #     print(e)
            self.action_list=[]

    def add_action(self,action):
        self.action_list[self.start_counter].append(action)

    async def notify_condition(self):
        print(self.action_condition,"notify")
        async with self.action_condition:
            self.action_condition.notify() 

    # def single_action(self,action):
    #     pass


class List_Action:
    def __init__(self,list_action) -> None:
        self.list_action:list[Action]=list_action

    def text(self,player):
        action_text=[]
        for action in self.list_action:
            text=action.text(player)
            if text!='':
                action_text.append(text)
        #action_text=[action.text(player) for action in self.list_action]
        actions=",".join(action_text)
        return f"action_list({actions})"
    
    def __repr__(self) -> str:
        return f"actions({','.join([str(i) for i in self.list_action])})"
    




class Creature_Start_Attack(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player",attack_obj:"Card|Player",show_hide:bool,state_self:tuple,state_attacted:tuple) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.attack_obj:"Card|Player"=attack_obj # store the selected_object card
        self.state_self:tuple=state_self
        self.state_attacted:tuple=state_attacted
    
    def text(self,player)-> str:
        state_self = f"state({','.join(map(str, self.state_self))})"

        state_attacted=f"state({','.join(map(str,self.state_attacted))})"
        return f"action(Creature_Start_Attack,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.attack_obj.text(player)},{state_self},{state_attacted}))"

class Creature_Prepare_Attack(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
       
    def text(self,player)-> str:
        
        return f"action(Creature_Prepare_Attack,parameters({self.object_hold.text(player)},{self.player.text(player)}))"

class Play_Cards(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        
       
    def text(self,player)-> str:
        
        return f"action(Play_Cards,parameters({self.object_hold.text(player)},{self.player.text(player)},showOBJ()))"


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
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card",color:str,type:str,final_state:tuple,buff:"Buff",show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        self.final_state:tuple=final_state
        self.buff:'Buff'=buff
        self.color=color
        self.type=type

    def text(self,player)-> str:
        
        final_state=f"state({','.join(map(str,self.final_state))})"
        
        select_text=self.check_inhand(self.object_selected,player)

        object_hold=self.check_inhand(self.object_hold,player)

        color=f"string({self.color})"
        buff=self.buff.text(player)
        return f"action(Add_Buff,parameters({object_hold},{self.player.text(player)},{select_text},{color},{self.type},{final_state},{buff}))"
    
class Lose_Buff(Select_Object):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card",final_state:tuple,buff:"Buff",show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        self.final_state:tuple=final_state
        self.buff:'Buff'=buff
       

    def text(self,player)-> str:
        final_state=f"state({','.join(map(str,self.final_state))})"
        
        select_text=self.check_inhand(self.object_selected,player)

        object_hold=self.check_inhand(self.object_hold,player)

        
        buff=self.buff.text(player)
        return f"action(Lose_Buff,parameters({object_hold},{self.player.text(player)},{select_text},{final_state},{buff}))"
    


class Attack_To_Object(Select_Object):#这种伤害自己的随从是不会受伤的
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",color:str,type:str,final_state:"tuple|list") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        self.color=color
        self.type=type
        self.final_state=final_state
    def text(self,player)-> str:
        final_state=f"state({','.join(map(str,self.final_state))})"
        color=f"string({self.color})"
        return f"action(Attack_To_Object,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.object_selected.text(player)},{color},{self.type},{final_state}))"
    

class Cure_To_Object(Select_Object):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",color:str,type:str,final_state:"tuple|list") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        self.color=color
        self.type=type
        self.final_state=final_state
    def text(self,player)-> str:
        final_state=f"state({','.join(map(str,self.final_state))})"
        color=f"string({self.color})"
        return f"action(Cure_To_Object,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.object_selected.text(player)},{color},{self.type},{final_state}))"
    
class Point_To(Select_Object):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        

    def text(self,player)-> str:
        
        return f"action(Point_To,parameters({self.object_hold.text(player)},{self.player.text(player)},{self.object_selected.text(player)}))"
    
class Gain_Card(Select_Object):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        
    def text(self,player)-> str:
        text_object_selected=self.object_selected.text(player,self.show_hide)
        return f"action(Gain_Card,parameters({self.object_hold.text(player)},{self.player.text(player)},{text_object_selected}))"
    

class Lose_Card(Select_Object):
    def __init__(self,object_hold:"Card|Player",player:"Player",selected_object:"Card|Player",show_hide:bool) -> None:
        self.show_hide:bool=show_hide # true show ,false hide
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card
        self.object_selected:"Card|Player"=selected_object # store the selected_object card
        
    def text(self,player)-> str:
        text_object_selected=self.object_selected.text(player,self.show_hide)
        return f"action(Lose_Card,parameters({self.object_hold.text(player)},{self.player.text(player)},{text_object_selected}))"
    

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

    def text(self,player:"Player")-> str:
        if player.name!=self.player.name:
            return ''
        mana=f"state({','.join(map(str,self.mana))})" 
        return f"action(Change_Mana,parameters({self.object_hold.text(player)},{self.player.text(player)},{mana}))"


class Win(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card

    def text(self,player:"Player")-> str:
        if player.name!=self.player.name:
            return ''
        return f"action(Win,parameters({self.object_hold.text(player)},{self.player.text(player)}))"

class Lose(Action):
    def __init__(self,object_hold:"Card|Player",player:"Player") -> None:
        
        self.object_hold:"Card|Player"=object_hold # store the controled card
        self.player:"Player"=player # who use the card

    def text(self,player:"Player")-> str:
        if player.name!=self.player.name:
            return ''
        return f"action(Lose,parameters({self.object_hold.text(player)},{self.player.text(player)}))"





