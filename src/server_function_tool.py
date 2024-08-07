from fastapi import FastAPI, Body,Depends, Form, HTTPException, Response, Request, status,APIRouter,WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from cryptography.fernet import Fernet



from pydantic import BaseModel

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
