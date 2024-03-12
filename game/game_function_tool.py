
import os
import json



from pydantic import validate_call,BaseModel
from typing_extensions import Literal
#from pycards import *




ORGPATH=os.path.dirname(os.path.abspath("/Users/xuanpeichen/Desktop/code/python/openai/server.py"))

def validate_all_methods(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, validate_call(attr_value))
    return cls


@validate_call
def send_select_request(type:str,number:int):
    return type

def check_select_valid(selected_object):
    return 

@validate_call
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

    def new_decorator(func):
        def new_func(self,*args, **kwargs):
            objects=send_select_request(type,number) if type else []
            kwargs[key_word] = objects
            def prepared_function():
                func(self,*args,**kwargs)
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



if __name__=="__main__":

    pass