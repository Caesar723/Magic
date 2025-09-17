from fastapi import FastAPI, Body,Depends, Form, HTTPException, Response, Request, status,APIRouter,WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from cryptography.fernet import Fernet



from pydantic import BaseModel,constr
from typing import Optional,Literal

import os
import json
import random
from datetime import datetime
import aiofiles





class CustomStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        if path.endswith(".py"):  # 检查是否为 .py 文件
            return Response(status_code=404)  # 不提供 .py 文件
        return await super().get_response(path, scope)

class Image_login_slider(BaseModel):
    image_url:list
    image_story:list

class Packs_by_player(BaseModel):
    image_url:list
    packs_id:list

class Cards_draw(BaseModel):#type,name,type_card,rarity,content,image_path
    type_color_background:list
    type_card:list#creature land...
    rarity:list
    content:list
    image_url:list
class PackData(BaseModel):
    id: int
    name:str
    name_id: int

class Page_Info(BaseModel):
    offset:int
    type_card:str
    color_card:str# colorless,red,green,blue,black,white

class Deck_Info(BaseModel):
    data:str


class Deck_splited(BaseModel):
    name:str
    type_card:str
    quantity:int

class Deck_Response(BaseModel):
    id:int
    content:list

class Deck_selected(BaseModel):
    id:int
    name:str

class Task_Data(BaseModel):
    id:int
    name:str
    description:str
    progress:int
    total_steps:int
    gold_reward:int

class Task_Data_List(BaseModel):
    task_data_list:list[Task_Data]

class Studio_Card_Data(BaseModel):
    init_name:str
    init_type:Literal["Creature","Land","Instant","Sorcery"]
    init_mana_cost:constr(pattern=r"^$|^\d+$|^\d+[URWBG]+$|^[URWBG]+$")
    init_color:Literal["colorless","blue","gold","black","red","green"]
    init_type_card:str
    init_rarity:Literal["Common","Uncommon","Rare","Mythic Rare"]
    init_content:str
    init_image_path:str
    init_keyword_list:list[str]
    select_object_range:Optional[str] = None
    when_start_turn_function:Optional[str] = None
    when_end_turn_function:Optional[str] = None
    when_kill_creature_function:Optional[str] = None
    when_a_creature_die_function:Optional[str] = None
    when_an_object_hert_function:Optional[str] = None
    aura_function:Optional[str] = None

class Studio_Creature_Data(Studio_Card_Data):
    init_actual_live:int
    init_actual_power:int
    init_type_creature:str
    when_enter_battlefield_function:Optional[str] = None
    when_leave_battlefield_function:Optional[str] = None
    when_die_function:Optional[str] = None
    when_harm_is_done_function:Optional[str] = None
    when_being_treated_function:Optional[str] = None
    when_become_attacker_function:Optional[str] = None
    when_become_defender_function:Optional[str] = None
    when_start_attcak_function:Optional[str] = None
    when_start_defend_function:Optional[str] = None
class Studio_Land_Data(Studio_Card_Data):
    # generate_mana_function:Optional[str] = None
    when_enter_battlefield_function:Optional[str] = None
    when_clicked_function:Optional[str] = None

class Studio_Instant_Data(Studio_Card_Data):
    is_undo:bool
    card_ability_function:Optional[str] = None
    
class Studio_Sorcery_Data(Studio_Card_Data):
    card_ability_function:Optional[str] = None

key = Fernet.generate_key()
cipher_suite = Fernet(key)
ORGPATH=os.path.dirname(os.path.abspath(__file__))

def decrypt_data_by_StaticFiles_server(encrypted_data:str)->str:
    try:
        encrypted_data=encrypted_data.encode("utf-8")
        decrypted_data=cipher_suite.decrypt(encrypted_data)
        return (decrypted_data).decode("utf-8")
    except:
        print("do not login",encrypted_data)
    

def encrypt_data_by_StaticFiles_server(text:str)->str:
        encrypted_data=cipher_suite.encrypt(text.encode("utf-8"))
        return (encrypted_data).decode("utf-8")

def get_time()->str:
        return str(datetime.now().date())

def list_subdirectories(directory_path):
    """ 列出指定目录下的所有子文件夹 """

    subdirectories = [d for d in os.listdir(directory_path)
                      if os.path.isdir(os.path.join(directory_path, d))]
    return subdirectories

async def get_five_random_image()->Image_login_slider:
     
    urls=[]
    stories=[]
    cards=list_subdirectories(f"{ORGPATH}/cards/creature")
    for i in range(5):
        card=cards[random.randint(0,len(cards)-1)]
        async with aiofiles.open(f"{ORGPATH}/cards/creature/{card}/data.json", 'r') as file:
            content = await file.read()
            data = json.loads(content)
        urls.append(encrypt_data_by_StaticFiles_server(f"src/cards/creature/{card}/image.jpg"))
        stories.append(data["Story Background"])
    return Image_login_slider(image_url=urls,image_story=stories)
     

def get_current_user_socket(database):
    async def get_current_user_actural(websocket: WebSocket):
        
        encrypted_data = websocket.cookies.get("mycookie")
       
        cookie_mess=decrypt_data_by_StaticFiles_server(encrypted_data)
        
        if not cookie_mess or cookie_mess==None:
            return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
        dic_mess=json.loads(cookie_mess)
        username=dic_mess["username"]
        password=dic_mess["password"]
        if username.split("_")[0]=="demo" and password=="demo":
            return username
        if await database.check_username_exists(username,password):# type: ignore
            return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
            
        return username
    return get_current_user_actural

def get_current_user(database):
    async def get_current_user_actural(request: Request):
       
        encrypted_data = request.cookies.get("mycookie")
        cookie_mess=decrypt_data_by_StaticFiles_server(encrypted_data)
        
        if not cookie_mess or cookie_mess==None:
            return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
        dic_mess=json.loads(cookie_mess)
        username=dic_mess["username"]
        password=dic_mess["password"]
        
        if await database.check_username_exists(username,password):# type: ignore
            return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
            
        return username
    return get_current_user_actural

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

def process_card_dict(data,card):
    if card['type']=="land":
        result_dict={
            "Name":card['name'],
            "Rarity": card['rarity'],
            "Ability":data["Ability"],
            "Background_url":check_type(data["Type"]),
            "Type_card":card['type'],
            "Image_url":card["relative_url"]+"/image.jpg"
        }
    elif card['type']=="creature":
        result_dict={
            "Name":card['name'],
            "Rarity": card['rarity'],
            "Ability":data["Ability"],
            "Cost":data["Cost"],
            "Background_url":check_color(data["Cost"]),
            "Type_card":data['Type'],
            "Image_url":card["relative_url"]+"/image.jpg",
            "Power": data['Power'],
            "Toughness": data['Toughness']
        }
    else:
        result_dict={
            "Name":card['name'],
            "Rarity": card['rarity'],
            "Ability":data["Ability"],
            "Cost":data["Cost"],
            "Background_url":check_color(data["Cost"]),
            "Type_card":card['type'],
            "Image_url":card["relative_url"]+"/image.jpg"
        }
    return result_dict

def split_message_deck(message:str):
    type_dic={
        "Creature":"creature",
        "Instant":"Instant",
        "Land":"land",
        "Sorcery":"sorcery"
    }

    splited=message.split("|")
    deck_name=splited[0]
    result=[]
    for card in splited[1:]:
        card_name,card_type,quantity=card.split("+")
        quantity=int(quantity)
        card_type=type_dic[card_type]
        result.append(Deck_splited(name=card_name,type_card=card_type,quantity=quantity))
    return (deck_name,result)

async def store_card_in_cache(card_data,file,username):
    content = await file.read()
    code_function={
        "Creature":get_creature_code,
        "Land":get_land_code,
        "Instant":get_instant_code,
        "Sorcery":get_sorcery_code
    }
    type_card=card_data.init_type
    if type_card in code_function:
        path=f"user_cache/{type_card}/{card_data.init_name}__{username}"
        image_path=f"{path}/image.jpg"
        code_path=f"{path}/model.py"
        code=code_function[type_card](card_data,image_path)
        os.makedirs(path, exist_ok=True)
        async with aiofiles.open(code_path, 'w') as file:
            await file.write(code)

        async with aiofiles.open(image_path, 'wb') as file:
            await file.write(content)
    else:
        print("type not found")

Functions_Dict={
    "when_enter_battlefield_function":
"""
    @select_object("{select_object_range}",1)
    async def when_enter_battlefield(self,player,opponent,selected_object):
    {function_code}
""",
    "when_leave_battlefield_function":
"""
    async def when_leave_battlefield(self,player= None, opponent = None,name:str='battlefield'):
    {function_code}
""",
    "when_die_function":
"""
    async def when_die(self,player= None, opponent = None):
    {function_code}
""",
    "when_start_turn_function":
"""
    async def when_start_turn(self,player= None, opponent = None):
    {function_code}
""",
    "when_end_turn_function":
"""
    async def when_end_turn(self,player= None, opponent = None):
    {function_code}
""",
    "when_harm_is_done_function":
"""
    async def when_harm_is_done(self,card,value,player= None, opponent = None):
    {function_code}
""",
    "when_being_treated_function":
"""
    async def when_being_treated(self,card,value,player= None, opponent = None):
    {function_code}
""",
    "when_become_attacker_function":
"""
    async def when_become_attacker(self,player= None, opponent = None):
    {function_code}
""",
    "when_become_defender_function":
"""
    async def when_become_defender(self,player= None, opponent = None):
    {function_code}
""",
    "when_kill_creature_function":
"""
    async def when_kill_creature(self,card,player= None, opponent = None):
    {function_code}
""",
    "when_start_attack_function":
"""
    async def when_start_attack(self,card,player= None, opponent = None):
    {function_code}
""",
    "when_start_defend_function":
"""
    async def when_start_defend(self,card,player= None, opponent = None):
    {function_code}
""",
    "when_a_creature_die_function":
"""
    async def when_a_creature_die(self,card,player= None, opponent = None):
    {function_code}
""",
    "when_an_object_hert_function":
"""
    async def when_an_object_hert(self,card,value,player= None, opponent = None):
    {function_code}
""",
    "aura_function":
"""
    async def aura(self,player= None, opponent = None):
    {function_code}
""",
    "card_ability_function":
"""
    @select_object("{select_object_range}",1)
    async def card_ability(self,player,opponent,selected_object):
    {function_code}
""",
    "when_clicked_function":
"""
    async def when_clicked(self,player= None, opponent = None):
    {function_code}
""",
    "generate_mana_function":
"""
    def generate_mana(self) -> dict:
    {function_code}
""",    
}

def add_function_code(card_data_dict,codes):
    for function_name,function_code in Functions_Dict.items():
        
        if function_name in card_data_dict and card_data_dict[function_name]:
            func_code=card_data_dict[function_name].replace("\n","\n        ").replace("\t","    ")
            if function_name=="when_enter_battlefield_function" or function_name=="card_ability_function":

                codes+="\n"+function_code.format(function_code=func_code,select_object_range=card_data_dict["select_object_range"])
            else:
                codes+="\n"+function_code.format(function_code=func_code)
    return codes

def get_creature_code(card_data:Studio_Creature_Data,image_path:str):
    flag_str="\n"
    for keyword in card_data.init_keyword_list:
        flag_str+=f"        self.flag_dict['{keyword}']=True\n"
    codes=f"""
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.type_cards.instant import Instant,Instant_Undo
from game.type_cards.sorcery import Sorcery
from game.type_cards.land import Land
from game.buffs import StateBuff,CounterBuff,KeyBuff,Tap,Frozen,Indestructible,Infect


class {card_data.init_name}(Creature):
    def __init__(self,player) -> None:
        super().__init__(player)
        self.name="{card_data.init_name}"
        self.live={card_data.init_actual_live}
        self.power={card_data.init_actual_power}
        self.actual_live={card_data.init_actual_live}
        self.actual_power={card_data.init_actual_power} 

        self.type_creature="{card_data.init_type_creature}"
        self.type="{card_data.init_type}"

        self.mana_cost="{card_data.init_mana_cost}"
        self.color="{card_data.init_color}"
        self.type_card="{card_data.init_type_card}"
        self.rarity="{card_data.init_rarity}"
        self.content="{card_data.init_content}"
        self.image_path="{image_path}"
        {flag_str}
    """

    card_data_dict=card_data.dict()
    codes=add_function_code(card_data_dict,codes)
    return codes

def get_land_code(card_data:Studio_Land_Data,image_path:str):
    flag_str="\n"
    for keyword in card_data.init_keyword_list:
        flag_str+=f"        self.flag_dict['{keyword}']=True\n"
    codes=f"""
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant,Instant_Undo
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff,CounterBuff,KeyBuff,Tap,Frozen,Indestructible,Infect

class {card_data.init_name}(Land):
    def __init__(self,player) -> None:
        super().__init__(player)
        self.name="{card_data.init_name}"
        self.type="{card_data.init_type}"
        self.mana_cost="{card_data.init_mana_cost}"
        self.color="{card_data.init_color}"
        self.type_card="{card_data.init_type_card}"
        self.rarity="{card_data.init_rarity}"
        self.content="{card_data.init_content}"
        self.image_path="{image_path}"
        {flag_str}
    """
    card_data_dict=card_data.dict()
    codes=add_function_code(card_data_dict,codes)
    return codes

def get_instant_code(card_data:Studio_Instant_Data,image_path:str):
    flag_str="\n"
    for keyword in card_data.init_keyword_list:
        flag_str+=f"        self.flag_dict['{keyword}']=True\n"
    codes=f"""
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.type_cards.land import Land
from game.type_cards.instant import Instant,Instant_Undo
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff,CounterBuff,KeyBuff,Tap,Frozen,Indestructible,Infect

class {card_data.init_name}({"Instant_Undo" if card_data.is_undo else "Instant"}):
    def __init__(self,player) -> None:
        super().__init__(player)
        self.name="{card_data.init_name}"
        self.type="{card_data.init_type}"
        self.mana_cost="{card_data.init_mana_cost}"
        self.color="{card_data.init_color}"
        self.type_card="{card_data.init_type_card}"
        self.rarity="{card_data.init_rarity}"
        self.content="{card_data.init_content}"
        self.image_path="{image_path}"
        {flag_str}
    """
    card_data_dict=card_data.dict()
    codes=add_function_code(card_data_dict,codes)
    return codes

def get_sorcery_code(card_data:Studio_Sorcery_Data,image_path:str):
    flag_str="\n"
    for keyword in card_data.init_keyword_list:
        flag_str+=f"        self.flag_dict['{keyword}']=True\n"
    codes=f"""
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.type_cards.land import Land
from game.type_cards.instant import Instant,Instant_Undo
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff,CounterBuff,KeyBuff,Tap,Frozen,Indestructible,Infect


class {card_data.init_name}(Sorcery):
    def __init__(self,player) -> None:
        super().__init__(player)
        self.name="{card_data.init_name}"
        self.type="{card_data.init_type}"
        self.mana_cost="{card_data.init_mana_cost}"
        self.color="{card_data.init_color}"
        self.type_card="{card_data.init_type_card}"
        self.rarity="{card_data.init_rarity}"
        self.content="{card_data.init_content}"
        self.image_path="{image_path}"
        {flag_str}
    """
    card_data_dict=card_data.dict()
    codes=add_function_code(card_data_dict,codes)
    return codes
