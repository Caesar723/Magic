from fastapi import Depends,APIRouter, Request
from typing import TYPE_CHECKING
import socket



import numpy as np
import os
from fastapi import UploadFile, File,HTTPException,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,StreamingResponse,Response,FileResponse
import asyncio


from server_function_tool import *
from game.rogue.rogue_manager import Rogue_Manager
from game.rlearning.utils.model import get_class_by_name
if TYPE_CHECKING:
    from database import DataBase
    from security import Security
    from game.room_server import RoomServer




def get_router(
    ras:"Security",
    database:"DataBase",
    room_server:"RoomServer",
    templates:"Jinja2Templates"
) -> APIRouter:

    router = APIRouter(prefix="/rogue")
    rogue_manager=Rogue_Manager()

    # 从环境变量读取
    @router.get("/rogue_map")
    async def rogue_map(request: Request, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username

        return templates.TemplateResponse("webpages/rogue/rogue.html",{"request": request})

    @router.post("/initinal_room")
    async def initinal_room(deck:Deck_selected, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username
        if await database.get_rogue_room(username):
            return {"state":"already in room"}

        deck_detail=await database.check_deck_real(deck.name,deck.id,username)
        rogue_room=rogue_manager.initinal_room(username,deck_detail)
        await database.create_rogue_room(rogue_room)
        return {"state":"success"}

    @router.post("/open_shop")
    async def open_shop(request: Request,data:NodeInfoRogue, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username
        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}
        node=rogue_manager.get_node_by_id(rogue_room["map_detail"]["map_structure"],data.node_id)
        if not node:
            return {"state":"not in room"}
        if node["name"]!="shop" and node["status"]!="current":
            return {"state":"not a shop"}
        shop_info=rogue_manager.node_to_json(node,rogue_room,hide=False)
        return {"state":"success","shop_info":shop_info}

    @router.post("/close_shop")
    async def close_shop(request: Request, data:NodeInfoRogue, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username
        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}
        node=rogue_manager.get_node_by_id(rogue_room["map_detail"]["map_structure"],data.node_id)
        if node["name"]=="shop":
            await enter_routine(data.node_id,username)
            return {"state":"success"}
        else:
            return  {"state":"not in room"}

    @router.post("/shop_buy")
    async def shop_buy(request: Request,data:ShopBugRogue, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username
        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}
        node=rogue_manager.get_node_by_id(rogue_room["map_detail"]["map_structure"],data.shop_id)
        if node["name"]=="shop":
            item=rogue_manager.get_shop_item_by_id(node,data.item_id)
            current_currency=int(rogue_room["profile"]["currency"])
            if item is not None and item["type"]=="treasure" and not item["is_selled"]:
                
                item_class=get_class_by_name(item["class_name"])
                item_spend=int(item_class.price)
                if current_currency>=item_spend:
                    await database.buy_shop_item(username,data.shop_id,round(current_currency-item_spend),data.item_id)
                    await database.add_treasure_to_rogue_room(username,item["class_name"])

                    return {"state":"success"}
                else:
                    return {"state":"not enough currency"}


            elif item is not None and item["type"]=="card_batch" and not item["is_selled"]:
                item_class=get_class_by_name(item["class_name"])
                item_spend=int(item_class.price)
                if current_currency>=item_spend:
                    
                    #await database.buy_shop_item(username,data.shop_id,round(current_currency-item_spend),data.item_id)
                    rogue_room["profile"]["currency"]=round(current_currency-item_spend)
                    item["is_selled"]=True
                    item_class.put_card_to_deck(rogue_room["profile"]["deck_detail"])
                    await database.update_rogue_room(username,rogue_room)
                    return {"state":"success"}
                else:
                    return {"state":"not enough currency"}

            elif item is not None and item["type"]=="live" and not item["is_selled"]:
                
                item_spend=int(item["price"])
                if current_currency>=item_spend:
                    
                    #await database.buy_shop_item(username,data.shop_id,round(current_currency-item_spend),data.item_id)
                    rogue_room["profile"]["max_life"]+=int(item["live"])
                    rogue_room["profile"]["currency"]=round(current_currency-item_spend)
                    item["is_selled"]=True
                    await database.update_rogue_room(username,rogue_room)
                    return {"state":"success"}
                else:
                    return {"state":"not enough currency"}
            else:
                return {"state":"not in room"}

    @router.post("/shop_sell")
    async def shop_sell(request: Request, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username

    @router.post("/get_profile_info")
    async def get_profile_info(request: Request, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username
        
        rogue_room=await database.get_rogue_room(username)

        return {
            "currency":rogue_room["profile"]["currency"],
            "max_life":rogue_room["profile"]["max_life"],
            "level":rogue_room["map_detail"]["level"],
        }

        
    @router.post("/map_info")
    async def map_info(request: Request, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username

        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}

        map_structure=rogue_room["map_detail"]["map_structure"]

        return rogue_manager.to_json(map_structure,rogue_room)


    @router.post("/treasure_info")
    async def treasure_info(request: Request, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username

        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}

        treasures=rogue_room["profile"]["treasures"]
        return rogue_manager.treasure_to_json(treasures)

    @router.post("/select_routine")
    async def select_routine(request: Request,data:NodeInfoRogue, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username
        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}
        node=rogue_manager.get_node_by_id(rogue_room["map_detail"]["map_structure"],data.node_id)
        if not node:
            return {"state":"not in room"}
        if node["status"]=="current":
            layer=rogue_manager.get_current_layer(rogue_room["map_detail"]["map_structure"],data.node_id)
            for current_node in layer:
                if current_node["id"]!=data.node_id:
                    await database.update_rogue_status(username,current_node["id"],"locked")
                    #if count==0:return {"state":"failed"}
            return {"state":"success"}
        else:
            return {"state":"not a current node"}

    #@router.post("/enter_routine")
    async def enter_routine(node_id:str, username: str):
        if type(username)==RedirectResponse:
            return username
        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}
        node=rogue_manager.get_node_by_id(rogue_room["map_detail"]["map_structure"],node_id)
        if not node:
            return {"state":"not in room"}
        if node["status"]=="current":
            next_layer=rogue_manager.get_next_node_layer(rogue_room["map_detail"]["map_structure"],node_id)
            for next_node in next_layer:  
                count=await database.update_rogue_status(username,next_node["id"],"current")
                if count==0:return {"state":"failed"}
            if next_layer==[]:
                result=rogue_manager.room_progress(rogue_room)
                if result[0]:
                    await database.update_rogue_level(username,result[1],result[2])
                    return {"state":"success"}
                else:
                    print("game end")
                    await database.delete_rogue_room(username)
                    return {"state":"end"}
                    
            count=await database.update_rogue_status(username,node_id,"completed")
            if count==0: return {"state":"failed"}
                
            return {"state":"success"}
        else:
            return {"state":"not a current node"}

    @router.post("/routine_info")
    async def routine_info(request: Request, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username


    @router.post("/open_event")
    async def open_event(request: Request, data:NodeInfoRogue, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username
        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}
        node=rogue_manager.get_node_by_id(rogue_room["map_detail"]["map_structure"],data.node_id)
        if not node:
            return {"state":"not in room"}
        if node["name"]!="event":
            return {"state":"not a event"}
        event_info=rogue_manager.node_to_json(node,rogue_room,hide=False)
        return {"state":"success","event_info":event_info}

    

    @router.post("/battle")
    async def battle(request: Request,data:NodeInfoRogue, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username
        
        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}
        node=rogue_manager.get_node_by_id(rogue_room["map_detail"]["map_structure"],data.node_id)
        if not node or node["name"]!="battle":
            return {"state":"not in room"}

        if room_server.check_client_in_room(username):
            return {"state":"find!"}
        rogue_info=rogue_manager.room_to_rogue_info(node,rogue_room)
        deck=rogue_manager.room_to_deck_detail(rogue_room)

        async def game_end_success():
            await database.add_currency_to_rogue_room(username,rogue_info["agent_win_price"])
            await enter_routine(data.node_id,username)
            return {"state":"success"}

        async def game_end_fail():
            await database.delete_rogue_room(username)
            return {"state":"success"}
        rogue_info["game_end_success_function"]=game_end_success
        rogue_info["game_end_fail_function"]=game_end_fail
        
        client_detail=(deck,username)
        await room_server.create_new_rogue_room(client_detail,rogue_info)
        return {"state":"find!"}
        #rogue_info["enter_routine"]=enter_routine(data.node_id,username)

        
        
       

    @router.post("/get_cards_info")
    async def get_cards_info(request: Request, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username
        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}
        cards=rogue_room["profile"]["deck_detail"]
        return {"state":"success","cards_info":rogue_manager.cards_to_json(cards)}

    @router.post("/select_event_option")
    async def select_event_option(request: Request, data:OptionSelectRogue, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username

        rogue_room=await database.get_rogue_room(username)
        if not rogue_room:
            return {"state":"not in room"}
        node=rogue_manager.get_node_by_id(rogue_room["map_detail"]["map_structure"],data.event_id)
        if not node or node["name"]!="event":
            return {"state":"not in room"}
        event_class=get_class_by_name(node["event"])
        if not event_class or data.option_index>=len(event_class.options):
            return {"state":"not a event"}
        if event_class.options[data.option_index]["valid_check"](rogue_room):
            event_class.options[data.option_index]["function"](rogue_room)
            await database.update_rogue_room(username,rogue_room)

            await enter_routine(data.event_id,username)
            return {"state":"success"}
        else:
            return {"state":"event can't select"}


    @router.post("/give_up_rogue")
    async def give_up_rogue(request: Request, username: str = Depends(get_current_user(database))):
        if type(username)==RedirectResponse:
            return username
        await database.delete_rogue_room(username)
        return {"state":"success"}
   
    
    return router

    