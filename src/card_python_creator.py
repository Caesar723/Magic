
import os
import json


ORGPATH=os.path.dirname(os.path.abspath(__file__))

def get_dir_names(path):
    arr=os.listdir(path)
    try:
        arr.remove(".DS_Store")
    except:pass
    return arr


def initinal_init_file():
    directory_path=f"{ORGPATH}/pycards"
    types=('creature','Instant','land','sorcery')
    with open(f"{ORGPATH}/pycards/__init__.py",'w') as f:
        
        for type in types:
            print(get_dir_names(f'{directory_path}/{type}'))
            for name in get_dir_names(f'{directory_path}/{type}'):
                if "model.py" in get_dir_names(f'{directory_path}/{type}/{name}'):
                    f.write(f"from .{type}.{name}.model import {name} as {name}_{type.upper()}  \n")


def check_color(cost):
    if cost:
        color_dict={
            "U":"blue",
            "W":"gold",
            "B":"black",
            "R":"red",
            "G":"green"
        }
        if cost[-1] in color_dict:
            return color_dict[cost[-1]]
        else:
            return "colorless"
    else:
        return "colorless"
    
def check_type(type_color):
     color_dict={
         "Water":"blue",
         "Light":"gold",
         "Dark":"black",
         "Fire":"red",
         "Forest":"green",
         "Arcane":"colorless"
    }
     return color_dict[type_color]

def remove_py():
    directory_path=f"{ORGPATH}/cards/creature"
    for name in get_dir_names(directory_path):
        file_path=f"{directory_path}/{name}/model.py"
        if os.path.exists(file_path):
            os.remove(file_path)
        

def creature_creater():
    directory_path=f"{ORGPATH}/cards/creature"

    for name in get_dir_names(directory_path):
        with open(f"{directory_path}/{name}/data.json", 'r') as file:
            data = json.load(file)

        class_name=name_replace(data["Name"])

        color=check_color(data["Cost"])
        ability=data["Ability"].replace("\"","\\\"")
        content=f"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class {class_name}(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="{data["Name"]}"
        self.live:int={data["Toughness"]}
        self.power:int={data["Power"]}
        self.actual_live:int={data["Toughness"]}
        self.actual_power:int={data["Power"]}

        self.type_creature:str="{data["Type"]}"
        self.type:str="Creature"

        self.mana_cost:str="{data["Cost"]}"
        self.color:str="{color}"
        self.type_card:str="{data["Type"]}"
        self.rarity:str="{data["Rarity"]}"
        self.content:str="{ability}"
        self.image_path:str="cards/creature/{data["Name"]}/image.jpg"



        """
        path=f"{ORGPATH}/pycards/creature/{class_name}"
        if not os.path.exists(path):
            #print(path)
            os.makedirs(path)
            with open(f"{path}/model.py",'w') as f:
                f.write(content)

def instant_creater():
    directory_path=f"{ORGPATH}/cards/Instant"

    for name in get_dir_names(directory_path):
        with open(f"{directory_path}/{name}/data.json", 'r') as file:
            data = json.load(file)

        class_name=name_replace(data["Name"])

        color=check_color(data["Cost"])
        ability=data["Ability"].replace("\"","\\\"")
        content=f"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class {class_name}(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="{data["Name"]}"

        self.type:str="Instant"

        self.mana_cost:str="{data["Cost"]}"
        self.color:str="{color}"
        self.type_card:str="Instant"
        self.rarity:str="{data["Rarity"]}"
        self.content:str="{ability}"
        self.image_path:str="cards/Instant/{data["Name"]}/image.jpg"



        """
        path=f"{ORGPATH}/pycards/Instant/{class_name}"
        if not os.path.exists(path):
            #print(path)
            os.makedirs(path)
            with open(f"{path}/model.py",'w') as f:
                f.write(content)      

def sorcery_creater():
    directory_path=f"{ORGPATH}/cards/sorcery"

    for name in get_dir_names(directory_path):
        with open(f"{directory_path}/{name}/data.json", 'r') as file:
            data = json.load(file)

        class_name=name_replace(data["Name"])

        color=check_color(data["Cost"])
        ability=data["Ability"].replace("\"","\\\"")
        content=f"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class {class_name}(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="{data["Name"]}"

        self.type:str="Sorcery"

        self.mana_cost:str="{data["Cost"]}"
        self.color:str="{color}"
        self.type_card:str="Sorcery"
        self.rarity:str="{data["Rarity"]}"
        self.content:str="{ability}"
        self.image_path:str="cards/sorcery/{data["Name"]}/image.jpg"



        """
        path=f"{ORGPATH}/pycards/sorcery/{class_name}"
        if not os.path.exists(path):
            os.makedirs(path)
            with open(f"{path}/model.py",'w') as f:
                f.write(content) 

def land_creater():
    directory_path=f"{ORGPATH}/cards/land"
    for name in get_dir_names(directory_path):
        with open(f"{directory_path}/{name}/data.json", 'r') as file:
            data = json.load(file)

        class_name=name_replace(data["Name"])

        color=check_type(data["Type"])
        ability=data["Ability"].replace("\"","\\\"")
        content=f"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.game_function_tool import select_object


class {class_name}(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="{data["Name"]}"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="{color}"
        self.type_card:str="Land"
        self.rarity:str="{data["Rarity"]}"
        self.content:str="{ability}"
        self.image_path:str="cards/land/{data["Name"]}/image.jpg"



        """
        path=f"{ORGPATH}/pycards/land/{class_name}"
        if not os.path.exists(path):
            os.makedirs(path)
        
            with open(f"{path}/model.py",'w') as f:
                f.write(content) 

def name_replace(name:str):
    replace_list=('~!@#$%^&*()+`-={}|[]\\:";\'<>?,./ ')
    for char in replace_list:
        name=name.replace(char,"_")
    return name


def check_unmake_cards():
    from initinal_file import CARD_DICTION
    from game.type_cards.creature import Creature
    from game.type_cards.instant import Instant,Instant_Undo
    from game.type_cards.land import Land
    from game.type_cards.sorcery import Sorcery
    types=(Creature,Instant,Land,Sorcery)
    def get_card_info(card_class):
        card:"Creature|Instant|Land|Sorcery"=card_class(None)
        if issubclass(card_class,Creature):
            parameters={"Name":card.name,"Rarity":card.rarity,"Type":card.type,"Power/Toughness":f"{card.power}/{card.live}","Cost":card.mana_cost,"Ability":card.content}
        elif issubclass(card_class,Instant):
            parameters={"Name":card.name,"Rarity":card.rarity,"Type":card.type,"Cost":card.mana_cost,"Ability":card.content}
        elif issubclass(card_class,Land):
            parameters={"Name":card.name,"Rarity":card.rarity,"Type":card.type,"Cost":card.mana_cost,"Ability":card.content}
        elif issubclass(card_class,Sorcery):
            parameters={"Name":card.name,"Rarity":card.rarity,"Type":card.type,"Cost":card.mana_cost,"Ability":card.content}
        para_str="#".join([f"{key}:{value}" for key,value in parameters.items()])
        return para_str+"\n"
    for type in types:
        for card_class in type.__subclasses__():
            # if card_class!=Instant_Undo:
            #     obj=card_class(None)
            #     if obj.color=="colorless":
            #         print(card_class.__name__)
            if not get_overridden_methods(card_class,type):
                info=get_card_info(card_class)
                with open(f"{ORGPATH}/card_info/unmake_cards.txt",'a') as f:
                    f.write(info)



def get_overridden_methods(child_class, parent_class):
    overridden_methods = []
    for method in dir(child_class):
        if method.startswith('__') and method.endswith('__'):
            continue  # 忽略特殊方法
        if method in dir(parent_class) and callable(getattr(child_class, method)):
            if getattr(child_class, method) is not getattr(parent_class, method):
                overridden_methods.append(method)
    return overridden_methods


if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    check_unmake_cards()
    #remove_py()

    # creature_creater()
    # land_creater()
    # sorcery_creater()
    # instant_creater()

    
    # initinal_init_file()
    
