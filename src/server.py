from fastapi import FastAPI, Body,Depends, Form, HTTPException, Response, Request, status,APIRouter,WebSocket,UploadFile,File
from fastapi.responses import HTMLResponse, RedirectResponse,FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect
from typing import Union
from pydantic import ValidationError
import os
import aiofiles.os
import uuid

from server_function_tool import *
from database import DataBase
from security import Security
from game.room_server import RoomServer,Room
from game.studio_room import Studio_Room
from game.rogue.rogue import get_router
from initinal_file import CARD_DICTION
from packs import *
from tasks import TASK_DICT



app = FastAPI()
database=DataBase()
ras=Security()
room_server=RoomServer(database)
templates = Jinja2Templates(directory=f"{ORGPATH}")

app.include_router(get_router(ras,database,room_server,templates))

###cryptography

###
###set StaticFiles
app.mount("/webpages", StaticFiles(directory="src/webpages"), name="webpages")
app.mount("/cards", CustomStaticFiles(directory="src/cards"), name="cards")
app.mount("/packet", CustomStaticFiles(directory="src/packet"), name="packet")
app.mount("/treasures", CustomStaticFiles(directory="src/treasures"), name="treasures")
###





@app.post("/login")
async def login(username: str = Body(...), password: str = Body(...), response: Response = None):
        result=await database.check_password_match(username,password)
        if result=="matched":
            cookie_mess=json.dumps({"username":username,"password":password})
            encrypted_data=encrypt_data_by_StaticFiles_server(cookie_mess)
            response.set_cookie(key="mycookie",httponly=True, value=encrypted_data, max_age=2592000, path='/')
            return {"message": "Login successful"}
        elif result=="passward error":
            return {"message": "passward error"}
        elif result=="username error":
            return {"message": "username error"}
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/login")
async def login_form(request: Request):
        print(request)
        #await database.show_all_tables_info()
        return templates.TemplateResponse(f"/webpages/loginpage/login.html", {"request": request})


@app.get("/signup")
async def signup_form(request: Request):
        print(request)
        return templates.TemplateResponse(f"webpages/loginpage/signup.html", {"request": request})


@app.post("/signup")
async def signup(username: str = Body(...), password: str = Body(...), response: Response = None):
        #print(await database.check_username_exists(username))
        
        if await database.check_username_exists(username,password):
            
            result=await database.store_users_password_new_player(username,password)
            if result=="signup successful":
                await database.add_all_cards_to_player(username)
                await database.add_all_cards_to_player(username)
                await database.add_all_cards_to_player(username)
                
                await database.add_all_cards_to_player(username)

                await database.add_packs("Original",username,20)
                await database.add_packs("Green",username,10)
                await database.add_packs("Blue",username,10)
                await database.add_packs("Black",username,10)
                await database.add_packs("White",username,10)
                await database.add_packs("Red",username,10)
                
                await database.add_packs("Antiquities",username,10)
                await database.add_packs("Legend",username,10)

                await database.store_card(username,"Island","land",30)
                await database.store_card(username,"Forest","land",30)
                await database.store_card(username,"Mountain","land",30)
                await database.store_card(username,"Plains","land",30)
                await database.store_card(username,"Swamp","land",30)
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
         return await room_server.matching(client_detail)
    else:
        return {"state":"unvalid deck"}
   

@app.post("/matching_ai")
async def game_page(deck:Deck_selected, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        print(username)
        return username
    deck=await database.check_deck_real(deck.name,deck.id,username)
    client_detail=(deck,username)
    await room_server.create_new_pveroom(client_detail)
    return {"state":"find!"}


@app.get("/gaming_ai") 
async def game_page(request: Request, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        print(username)
        return username
    # deck=await database.check_deck_real(deck.name,deck.id,username)
    # client_detail=(deck,username)
    # await room_server.create_new_pveroom(client_detail)
    return templates.TemplateResponse(f"webpages/game_ai/gaming.html", { "request": request,"data": room_server.get_players_name(username)})

@app.post("/matching_demo")
async def game_page(request: Request, response: Response):
    data = request.cookies.get("mycookie")
    name=decrypt_data_by_StaticFiles_server(data)
    print(name)
    if not name or name==None:
        uid=str(uuid.uuid4())
        name=f"demo_{uid}"
        cookie_mess=json.dumps({"username":name,"password":"demo"})
        encrypted_data=encrypt_data_by_StaticFiles_server(cookie_mess)
        print(encrypted_data)
        response.set_cookie(key="mycookie",httponly=True, value=encrypted_data, max_age=2592000, path='/')
    else:
        name=json.loads(name)["username"]
    client_detail=("",name)
    await room_server.create_new_pvedemo_room(client_detail)
    return {"state":"find!"}

@app.get("/game_demo")
async def game_demo_page(request: Request):
   
    
    encrypted_data = request.cookies.get("mycookie")
    print(encrypted_data)
    cookie_mess=decrypt_data_by_StaticFiles_server(encrypted_data)
    
    if not cookie_mess or cookie_mess==None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    dic_mess=json.loads(cookie_mess)
    username=dic_mess["username"]
    #password=dic_mess["password"]
    
    return templates.TemplateResponse(f"webpages/game_ai/gaming.html", {"request": request, "data": room_server.get_players_name(username)})

@app.get("/game_replay")
async def game_replay_page(request: Request, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        print(username)
        return username
    return templates.TemplateResponse(f"webpages/game_replay/gaming.html", {"request": request, "data": room_server.get_players_name(username)})



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
    return templates.TemplateResponse(f"webpages/gaming_page/gaming.html", {"request": request, "data": room_server.get_players_name(username)})

@app.get("/studio")
async def studio_page(request: Request, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        print(username)
        return username
    return templates.TemplateResponse(f"webpages/studio/creating_page.html", {"request": request, "data": room_server.get_players_name(username)})

@app.post("/matching_studio")
async def studio_page(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        print(username)
        return username
    client_detail=("",username)
    await room_server.create_new_studio_room(client_detail)
    return {"opponent": "Agent1", "self": username}

@app.post("/delete_studio_room")
async def delete_studio_room(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    return room_server.delete_studio_room(username)
# @app.post("/players") 
# async def matching_delete(username: str = Depends(get_current_user(database))):
#     if type(username)==RedirectResponse:
#         return username
    
#     return room_server.get_players_name(username)

@app.websocket("/entering_game")
async def entering_game(websocket: WebSocket,username: str = Depends(get_current_user_socket(database))):#
    if type(username)==RedirectResponse:
        return username
    
    await websocket.accept()
    room:Room=room_server.find_player_room(username)
    if room=="no room found":
        return {"state":"no room found"}
    await room.set_socket(websocket,username)
    try:
        while room.gamming:
            data = await websocket.receive_text()
            await room.message_receiver(data)
    except WebSocketDisconnect as e:
        room.players_socket[username]=None
        print(f"WebSocket disconnected with code: {e.code}")
        if e.code == 1001:
            print("Connection closed by the client or server going away.")
    except Exception as e:
        await websocket.close()
        
        

@app.websocket("/select_object")
async def select_object(websocket: WebSocket,username: str = Depends(get_current_user_socket(database))):#
    if type(username)==RedirectResponse:
        return username
    await websocket.accept()
    print(websocket,username)
    room:Room=room_server.find_player_room(username)
    if room=="no room found":
        return {"state":"no room found"}
    player=room.set_select_socket(websocket,username)
    # while player.socket_connected_flag:
    #     #await websocket.send_text("select(all_roles)")
    await player.wait_selection_socket()
        
    

# @app.get("/tech_doc/zh")
# async def login_form(request: Request):
        
#         return templates.TemplateResponse(f"webpages/tech_doc/content.html", {"request": request})
@app.get("/tech_doc")
async def login_form(request: Request):
        
        return templates.TemplateResponse(f"webpages/tech_doc/content_En.html", {"request": request})

@app.get("/shop")
async def shop_page(request: Request, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    return templates.TemplateResponse(f"webpages/shop_page/shop.html", {"request": request})

@app.post("/shop/items")
async def shop_items(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    return await database.get_shop_items(Packs_Dict)

@app.post("/shop/buy")
async def shop_buy(packdata: PackData ,username: str = Depends(get_current_user(database))):
    print(packdata.name,packdata.id)
    if type(username)==RedirectResponse:
        return username
    return await database.buy_shop_items(packdata.id,packdata.name,username,Packs_Dict)


@app.get("/tech_doc/{lang}")
async def get_documentation(request: Request,lang: str):
    dict_lang={
        "zh":"webpages/tech_doc/content.html",
        "en":"webpages/tech_doc/content_En.html",
    }
    if lang in dict_lang:
        return templates.TemplateResponse(dict_lang[lang], {"request": request})
    else:
        return templates.TemplateResponse(f"webpages/tech_doc/content.html", {"request": request})

@app.post("/get_currency")
async def get_currency(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    currency=await database.get_currency(username)
    return {"currency":currency}

@app.post("/get_all_cards_name")
async def get_all_cards_name(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    
    result={}
    for key in CARD_DICTION.keys():
        name,types=key.split("_")
        if types not in result:
            result[types]=[]
        result[types].append(name)
    return {"card_names": result}


@app.post("/add_studio_card")
async def add_studio_card(datas: dict, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    try:
        type_dict={
            "Creature":Studio_Creature_Data,
            "Land":Studio_Land_Data,
            "Instant":Studio_Instant_Data,
            "Sorcery":Studio_Sorcery_Data
        }
        #datas=json.loads(datas)
        datas=type_dict[datas["init_type"]](**datas)
    except ValidationError as e:
        return {"state":"unsuccessful","error":str(e)}
    
    
    room=room_server.find_player_room(username)
    if isinstance(room,Studio_Room):
        room.add_studio_card(datas,username)
        return {"state":"successful"}
    else:
        return {"state":"no studio room found"}

@app.post("/submit_studio_card")
async def submit_studio_card(
    json_data: str = Form(...),  
    file: UploadFile = File(...), 
    username: str = Depends(get_current_user(database))):

    if type(username)==RedirectResponse:
        return username
    

    print(json_data)
    print(file)
    try:
        type_dict={
            "Creature":Studio_Creature_Data,
            "Land":Studio_Land_Data,
            "Instant":Studio_Instant_Data,
            "Sorcery":Studio_Sorcery_Data
        }
        datas=json.loads(json_data)
        datas=type_dict[datas["init_type"]](**datas)
    
        await store_card_in_cache(datas,file,username)
    except (ValidationError,Exception) as e:
        import traceback
        traceback.print_exc()
        return {"state":"unsuccessful","error":str(e)}
    
    return {"state":"successful"}

@app.get("/task")
async def task_page(request: Request, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    return templates.TemplateResponse(f"webpages/task_page/task.html", {"request": request})



@app.post("/get_task", response_model=Task_Data_List)
async def get_task(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    await database.check_tasks(username,TASK_DICT)
    return await database.get_tasks(username,TASK_DICT)

class RefreshTaskRequest(BaseModel):
    task_id: int
@app.post("/refresh_task", response_model=Task_Data)
async def refresh_task(request: RefreshTaskRequest,username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    return await database.refresh_task(request.task_id,username,TASK_DICT)


@app.post("/get_cards_path")
async def get_cards_path(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    
    root_paths={"creature":f"{ORGPATH}/cards/creature","land":f"{ORGPATH}/cards/land","instant":f"{ORGPATH}/cards/instant","sorcery":f"{ORGPATH}/cards/sorcery"}

    result=[]
    for key in root_paths.keys():
        cards_path=await aiofiles.os.listdir(root_paths[key])
        print(cards_path)
        for card in cards_path:
            result.append(f"{key}/{card}")
    return {"cards_path":result}

@app.post("/get_replay_records")
async def get_game_records(username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username

    folder_path=f"{ORGPATH}/game/game_records/{username}"
    if not os.path.exists(folder_path):
        return {"files": []}
    files=await aiofiles.os.listdir(folder_path)
    return {"files":files}
     
@app.get("/download/game_records/{filename}")
async def download_file(filename: str,username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        return username
    file_path=f"{ORGPATH}/game/game_records/{username}/{filename}"
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(path=file_path, filename=filename, media_type="application/octet-stream")

@app.get("/gaming_rogue") 
async def game_page(request: Request, username: str = Depends(get_current_user(database))):
    if type(username)==RedirectResponse:
        print(username)
        return username
    # deck=await database.check_deck_real(deck.name,deck.id,username)
    # client_detail=(deck,username)
    # await room_server.create_new_pveroom(client_detail)
    return templates.TemplateResponse(f"webpages/rogue/gaming.html", { "request": request,"data": room_server.get_players_name(username)})


def main():
    import uvicorn
    uvicorn.run(app, host="172.16.6.78", port=8000, ssl_keyfile="private.key", ssl_certfile="certificate.crt",reload=True)

if __name__=="__main__":
    main()
    pass
