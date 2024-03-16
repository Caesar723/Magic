from fastapi import FastAPI, Body,Depends, Form, HTTPException, Response, Request, status,APIRouter,WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse,FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os

from server_function_tool import *
from database import DataBase
from security import Security
from game.room_server import RoomServer,Room

from packs import *



app = FastAPI()
database=DataBase()
ras=Security()
room_server=RoomServer(database)
templates = Jinja2Templates(directory=f"{ORGPATH}")

###cryptography

###
###set StaticFiles
app.mount("/webpages", StaticFiles(directory="webpages"), name="webpages")
app.mount("/cards", CustomStaticFiles(directory="cards"), name="cards")
app.mount("/packet", CustomStaticFiles(directory="packet"), name="packet")
###





@app.post("/login")
async def login(username: str = Body(...), password: str = Body(...), response: Response = None):
        result=await database.check_password_match(username,password)
        if result=="matched":
            cookie_mess=json.dumps({"username":username,"password":password})
            encrypted_data=encrypt_data_by_StaticFiles_server(cookie_mess)
            response.set_cookie(key="mycookie",httponly=True, value=encrypted_data, max_age=1800, path='/')
            return {"message": "Login successful"}
        elif result=="passward error":
            return {"message": "passward error"}
        elif result=="username error":
            return {"message": "username error"}
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/login")
async def login_form(request: Request):
        print(request)
        await database.show_all_tables_info()
        return templates.TemplateResponse(f"/webpages/loginpage/login.html", {"request": request})


@app.get("/signup")
async def signup_form(request: Request):
        print(request)
        return templates.TemplateResponse(f"webpages/loginpage/signup.html", {"request": request})


@app.post("/signup")
async def signup(username: str = Body(...), password: str = Body(...), response: Response = None):
        #print(await database.check_username_exists(username))
        
        if await database.check_username_exists(username):
            
            result=await database.store_users_password_new_player(username,password)
            if result=="signup successful":
                await database.add_packs("Original",username,20)
                await database.add_packs("Green",username,1)
                await database.add_packs("Blue",username,1)
                
                await database.add_packs("Legend",username,3)
                #await database.show_all_tables_info()
                return {"message": "Sign up successful"}

        return {"message": "Sign up unsuccessful"}

@app.get("/")
async def protected_page(request: Request, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        print(username)
        return username
    
    return templates.TemplateResponse(f"/webpages/homepage/protectpage.html", {"request": request, "username": username})

@app.post("/login/cards_show")
async def login_return_cards(response: Response = None):
    return await get_five_random_image()

@app.get("/get-images/{encrypted_info_server}")
async def get_images(encrypted_info_server: str):
    # 解密信息
    decrypted_info = encrypt_data_by_StaticFiles_server(encrypted_info_server)  # 假设这是您的解密函数
    if decrypted_info is None:
        raise HTTPException(status_code=400, detail="Invalid encrypted information")
    
    return FileResponse(f"{decrypt_data_by_StaticFiles_server(encrypted_info_server)}")

@app.get("/draw_card")
async def draw_card_page(request: Request, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        print(username)
        return username
    return templates.TemplateResponse(f"webpages/draw_card/draw.html", {"request": request, "username": username})


@app.post("/get_packs_information")
async def return_packs_draw(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    #print(await database.get_player_packs(username))
    return await database.get_player_packs(username)

@app.post("/send_pack")
async def return_cards_draw(pack_data: PackData ,username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    pack=Packs_Dict[pack_data.name]()
    cards=await database.draw_cards(pack_data.id,pack_data.name_id,*pack.draw_cards(),username)
    #await database.show_all_tables_info()
    result=[]
    for card in cards:
        #/Users/xuanpeichen/Desktop/code/python/openai/cards/Instant/Veil of Serenity/data.json
        async with aiofiles.open(f"{ORGPATH}/{card['relative_url']}/data.json", 'r') as file:
            # 读取文件内容
            content = await file.read()
            # 解析JSON数据
            data = json.loads(content)
        result_dict=process_card_dict(data,card)
        result.append(result_dict)
    cards_json = json.dumps(result)
    
    return cards_json

@app.get("/deck_building")
async def deck_building_page(request: Request, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        print(username)
        return username
    return templates.TemplateResponse(f"webpages/deckpage/deck.html", {"request": request, "username": username})

@app.post("/deck_page")
async def return_cards_draw(Page_Info: Page_Info ,username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    
    max_limit=8
    cards=await database.page_cards(Page_Info.offset,max_limit,Page_Info.color_card,Page_Info.type_card,username)
    result=[]
    for card in cards:
        #/Users/xuanpeichen/Desktop/code/python/openai/cards/Instant/Veil of Serenity/data.json
        async with aiofiles.open(f"{ORGPATH}/{card['relative_url']}/data.json", 'r') as file:
            # 读取文件内容
            content = await file.read()
            # 解析JSON数据
            data = json.loads(content)
        result_dict=process_card_dict(data,card)
        result_dict["quantity"]=card['quality']
        result.append(result_dict)
    cards_json = json.dumps(result)
    
    return cards_json

@app.post("/send_deck")
async def store_deck(Deck_Info: Deck_Info ,username: str = Depends(get_current_user(database))):
    
    dectypted_data=ras.decrypt_with_aes(Deck_Info.data)
    
    splited_data=split_message_deck(dectypted_data)
    
    if (await database.check_cards_in_player(splited_data[1],username)):
        #print(dectypted_data)
        split=dectypted_data.split("|")
        name=split[0]
        cards="|".join(split[1:])
        await database.store_deck(name,cards,username)
        return {"state":"successful"}
    else:
        return  {"state":"unsuccessful"}
    

@app.post("/get_public_key")
async def get_public_key(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    result={"key":ras.public_key_pem}
    
    return result

@app.post("/get_decks_home")
async def get_decks_home(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    
    return await database.get_all_decks(username)



@app.post("/delete_deck")
async def get_decks_home(deck_info:Deck_selected,username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    state=await database.delete_decks(deck_info.name,deck_info.id,username)
    if state:
        return {"state":"successful"}
    else:
        return {"state":"unsuccessful"}


@app.post("/matching")
async def matching(deck:Deck_selected,username: str = Depends(get_current_user(database))):# 先检查现有的room，在检查现有的队列，如果都没有，把人放进队列里
    if type(username)==RedirectResponse:
        return username
    
    deck=await database.check_deck_real(deck.name,deck.id,username)
    client_detail=(deck,username)
    if deck:
         return room_server.matching(client_detail)
    else:
        return {"state":"unvalid deck"}
   




@app.post("/matching_delete")
async def matching_delete(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    
    return room_server.delete_matching(username)

@app.get("/gaming") 
async def game_page(request: Request, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        print(username)
        return username
    return templates.TemplateResponse(f"webpages/gaming_page/gaming.html", {"request": request, "username": username})



@app.websocket("/entering_game")
async def entering_game(websocket: WebSocket,username: str = Depends(get_current_user_socket(database))):#
    if type(username)==RedirectResponse:
        return username
    
    await websocket.accept()
    room:Room=room_server.find_player_room(username)
    room.set_socket(websocket,username)
    while True:
        data = await websocket.receive_text()
        print(data)
        await room.message_receiver(data)

@app.websocket("/select_object")
async def select_object(websocket: WebSocket,username: str = Depends(get_current_user_socket(database))):#
    if type(username)==RedirectResponse:
        return username
    await websocket.accept()
    room:Room=room_server.find_player_room(username)
        



def main():
    pass

main()
