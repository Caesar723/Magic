
import os
import json



from pydantic import validate_call,BaseModel
from typing_extensions import Literal
from typing import TYPE_CHECKING
import asyncio
import random


from game.type_action import actions

if TYPE_CHECKING:
    from game.card import Card
    from game.room import Room
    from game.player import Player
#from pycards import *




ORGPATH=os.path.dirname(os.path.abspath("/Users/xuanpeichen/Desktop/code/python/openai/server.py"))

def validate_all_methods(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, validate_call(attr_value))
    return cls



async def send_select_request(card:'Card',type:str,number:int,selection_random:bool=False):
    try:
        room=card.player.room
        player=card.player
        objects=[]
        if type:
            for i in range(number):
                async with player.selection_lock:
                    await player.send_text(f"select({type})")
                    data =await player.receive_text()# ...|player;区域;index
                    obj=get_object(data,room,type,card)
                    if obj:
                        if ("cancel"==obj and selection_random):
                            obj=random_select(player,type)
                        objects.append(obj)

            #return objects
        else:
            objects=await card.selection_step(player,player.opponent,selection_random)
            #return objects
        if ("cancel" in objects):
            raise asyncio.CancelledError("Client cancellation")
        else:
            return objects
    except asyncio.CancelledError:
        return "cancel"
    
def get_object(data:str,room:'Room',type:str,card:'Card'):#名字，选择类型（field或者cards），（场地名{self_battlefield,opponent_battlefield,self_landfield,opponent_landfield}或者player{self,oppo}），如果是场地index。cards直接index
    parameters=data.split("|")
    player:'Player'=room.players[parameters[0]]

    field_dict={
        "self_battlefield":player.battlefield,
        "opponent_battlefield":player.opponent.battlefield,
        "self_landfield":player.land_area,
        "opponent_landfield":player.opponent.land_area,
        
    }
    player_dict={
        "self":player,
        "oppo":player.opponent,
    }
    obj=''
    if parameters[1]=="field":#选择类型（field或者cards）
        if parameters[2] in field_dict:
            index=int(parameters[3])
            obj=field_dict[parameters[2]][index]
        elif parameters[2] in player_dict:
            obj= player_dict[parameters[2]]
    elif parameters[1]=="cancel":
        return "cancel"
    if obj and check_select_valid(player,obj,type):
        
        #room.action_processor.start_record()
        if card in player.battlefield or card in player.opponent.battlefield or card in player.land_area or card in player.opponent.land_area:
            room.action_processor.add_action(actions.Point_To(card,player,obj))
        else:
            room.action_processor.add_action(actions.Point_To(player,player,obj))
        #room.action_processor.end_record()
        return obj
    else:
        return False
    
    


def check_select_valid(player:'Player',selected_object,type_selection:str):
    self_player=player
    oppo_player=player.opponent
    
    type_dict={
        'all_roles':[self_player.battlefield,oppo_player.battlefield,oppo_player,self_player],
        'opponent_roles':[oppo_player.battlefield,oppo_player], 
        'your_roles':[self_player.battlefield,self_player],
        'all_creatures':[self_player.battlefield,oppo_player.battlefield],
        'opponent_creatures':[oppo_player.battlefield],
        'your_creatures':[self_player.battlefield],
        'all_lands':[self_player.land_area,oppo_player.land_area],
        'opponent_lands':[oppo_player.land_area],
        'your_lands':[self_player.land_area], 
    }
    type_player=type(self_player)

    if type_selection in type_dict:
        for element in type_dict[type_selection]:
            if isinstance(element,type_player)  :
                if selected_object==element:
                    return True
            else:
                #print(element)
                
                if selected_object in element:
                    return True
    return False
            
def random_select(player:'Player',type_selection:str):
    self_player=player
    oppo_player=player.opponent
    type_dict={
        'all_roles':[self_player.battlefield,oppo_player.battlefield,oppo_player,self_player],
        'opponent_roles':[oppo_player.battlefield,oppo_player], 
        'your_roles':[self_player.battlefield,self_player],
        'all_creatures':[self_player.battlefield,oppo_player.battlefield],
        'opponent_creatures':[oppo_player.battlefield],
        'your_creatures':[self_player.battlefield],
        'all_lands':[self_player.land_area,oppo_player.land_area],
        'opponent_lands':[oppo_player.land_area],
        'your_lands':[self_player.land_area], 
    }

    combined_list=[]
    for item in type_dict[type_selection]:
        if isinstance(item,type(player)):
            combined_list.append(item)
        else:
            combined_list+=item
    if combined_list:
        return random.choice(combined_list)
    else:
        return "cancel"



# def check_have_object(type):
#     pass

def select_object(type:Literal['all_roles',#分为两个阶段，准备阶段和使用阶段，询问选择对象为准备阶段，会返回一个function，调用这个function为使用阶段
                               'opponent_roles', #只有在creature的战吼，sorcery的打出的能力，和instant 打出能力时，会用到
                               'your_roles',
                               'all_creatures',
                               'opponent_creatures',
                               'your_creatures',
                               'all_lands',
                               'opponent_lands',
                               'your_lands',
                               ''],
                  number:int):
    
    
    key_word="selected_object"


    key_random="selection_random"

    def new_decorator(func):
        async def new_func(self:"Card",*args, **kwargs):
            if key_random in kwargs:
                self.player.future_function=asyncio.create_task(send_select_request(self,type,number,kwargs[key_random]))
            else:
                self.player.future_function=asyncio.create_task(send_select_request(self,type,number))
            objects=await self.player.future_function
            print(objects)
            if objects=="cancel":
                    return "cancel"
            kwargs[key_word] = objects
            async def prepared_function():
                await func(self,*args,**kwargs)
            return prepared_function
        return new_func
    return new_decorator



def get_dir_names(path):
    arr=os.listdir(path)
    try:
        arr.remove(".DS_Store")
    except:pass
    return arr

def get_cards_diction():
    
    from game.card import Card
    import pycards
    
    types=["creature","Instant","land","sorcery"]
    class_dict={}

    for type in types:
        directory_path=f"{ORGPATH}/cards/{type}"
        for name in get_dir_names(directory_path):

            class_name=name_replace(name)
            class_dict[class_name]=name

    result_dict={}
    for subclass in Card.__subclasses__():
        for card in subclass.__subclasses__():
            result_dict[f"{class_dict[card.__name__]}_{subclass.__name__}"]=card
    
    return result_dict

def name_replace(name:str):
    replace_list=('~!@#$%^&*()+`-={}|[]\\:";\'<>?,./ ')
    for char in replace_list:
        name=name.replace(char,"_")
    return name

def backup_instance_methods(instance):
    """备份对象中的所有方法"""
    instance._original_methods = {}
    for attr_name in dir(instance.__class__):
        attr = getattr(instance.__class__, attr_name)
        if callable(attr) and not attr_name.startswith("__"):
            ins_attr = getattr(instance, attr_name)
            instance._original_methods[attr_name] = ins_attr
       

def reset_instance_methods(instance):
    """重置对象的方法到原始状态"""
    for attr_name, attr_value in instance._original_methods.items():
        setattr(instance, attr_name, attr_value)
   

if __name__=="__main__":

    pass