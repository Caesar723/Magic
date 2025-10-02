import random
import uuid
from types import SimpleNamespace

if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
from game.game_function_tool import ORGPATH
from game.rlearning.utils.model import get_class_by_name
from game.rogue.rogue_dict import ROGUE_AGENTS_DICT,ROGUE_TREASURE_DICT,ROGUE_EVENT_DICT
from initinal_file import CARD_DICTION

class Rogue_Manager:
    
    def __init__(self):
        self.agents_info=ROGUE_AGENTS_DICT

        self.treasure_info=ROGUE_TREASURE_DICT

        self.event_info=ROGUE_EVENT_DICT

    def deck_detail_to_dict(self,deck_detail):
        result=[]
        for element in deck_detail.split("|"):
            name,type_card,number=element.split("+")
            result.append({
                "name":name,
                "type_card":type_card,
                "number":number,
            })
        return result
    
    def initinal_room(self,username,deck_detail):
        map_structure=self.create_map(level=0)
        return {
            "_id": username,
            "username":username,
            "profile": {
                "deck_detail": self.deck_detail_to_dict(deck_detail),
                "treasures": [
            
                ],
                "max_life": 20,
                "currency": 10,#初始 10 货币
                
            },
            "map_detail":{
                "level":0,
                "map_structure":map_structure,
                
            },
            "extra_info": {
                
            }

        }


    def create_map(self,level=0):
        map=[[{"name":"Start","status":"completed","id":str(uuid.uuid4())}]]
        previous_len=len(map[0])
        for i in range(random.randint(6,10)):
            if previous_len==2:
                branchs=[self.create_node(False,level) for _ in range(random.choice([1,2]))]
            elif previous_len==3:
                branchs=[self.create_node(False,level) for _ in range(random.choice([1,3]))]
            else:
                branchs=[self.create_node(False,level) for _ in range(random.choice([1,2,3]))]
            previous_len=len(branchs)
            map.append(branchs)
        map.append([self.create_node(True,level)])

        for node in map[1]:
            node["status"]="current"#"completed"#"current"
        return map


    

    def create_node(self,is_boss:bool,level=0):
        levels=["low_level","middle_level","high_level"]
        if is_boss:
            agent_info=self.agents_info["agent_"+levels[level]]
            agent=random.choice(agent_info["config_lists_boss"])
            result={
                "name":"battle",
                "status":"locked",
                "agent_name":agent["name"],
                "agent_config":agent["config_path"],
                "agent_max_life":agent_info["boss_max_life"],
                "agent_win_price":random.randint(agent_info["boss_win_price_min"],agent_info["boss_win_price_max"]),
                "avatar":agent["avatar"],
                "description":agent["description"],
                "treasures":[],
            }
        else:
            types=["battle","shop","event"]
            types_percentage=[0.4,0.25,0.35]
            type_=random.choices(types,types_percentage)[0]
            if type_=="battle":
                agent_info=self.agents_info["agent_"+levels[level]]
                agent=random.choice(agent_info["config_lists_monster"])
                result={
                    "name":type_,
                    "status":"locked",
                    "agent_name":agent["name"],
                    "agent_config":agent["config_path"],
                    "agent_max_life":agent_info["monster_max_life"],
                    "agent_win_price":random.randint(agent_info["win_price_min"],agent_info["win_price_max"]),
                    "avatar":agent["avatar"],
                    "description":agent["description"],
                    "treasures":[],
                }
            elif type_=="shop":
                treasure_info=self.treasure_info[levels[level]]
                treasures=random.sample(treasure_info["treasure_list"],3)
                treasures=[{"id":str(uuid.uuid4()),"class_name":treasure,"type":"treasure","is_selled":False} for treasure in treasures]
                result={
                    "name":type_,
                    "status":"locked",
                    "items":treasures
                }
            elif type_=="event":
                event_info=self.event_info[levels[level]]
                event=random.choice(event_info["event_list"])
                result={
                    "name":type_,
                    "status":"locked",
                    "event":event
                }
        result["id"]=str(uuid.uuid4())
        return result

    def to_json(self,room_structure:dict,room_info:dict):
        return [[self.node_to_json(node,room_info) for node in nodes] if len(nodes)>1 else self.node_to_json(nodes[0],room_info) for nodes in room_structure]

    def room_to_rogue_info(self,battle_node:dict,room_info:dict):

        return {
            "self_max_life":room_info["profile"]["max_life"],
            "treasures":room_info["profile"]["treasures"],
            "agent_config":battle_node["agent_config"],
            "agent_max_life":battle_node["agent_max_life"],
            "agent_win_price":battle_node["agent_win_price"],
            "extra_info":room_info["extra_info"],
            "agent_treasures":battle_node["treasures"]
        }

    def room_to_deck_detail(self,room_info:dict):
        deck_list=room_info["profile"]["deck_detail"]
        result=[]
        for deck in deck_list:
            result.append(deck["name"]+"+"+deck["type_card"]+"+"+str(deck["number"]))
        return "|".join(result)


    def node_to_json(self,node:dict,room_info:dict,hide:bool=True):
        if node["name"]=="Start":
            return {
                "id":node["id"],
                "name":node["name"],
                "status":"completed",
            }
        
        if hide and (node["status"]=="locked" or (node["status"]=="current" and node["name"]!="battle")):
            return {
                "id":node["id"],
                "name":node["name"],
                "status":node["status"],
            }
        else:
            if node["name"]=="battle":
                return {
                    "id":node["id"],
                    "name":node["name"],
                    "status":node["status"],
                    "agent_name":node["agent_name"],
                    "agent_max_life":node["agent_max_life"],
                    "agent_win_price":node["agent_win_price"],
                    "avatar":node["avatar"],
                    "description":node["description"],
                }
            elif node["name"]=="shop":
                treasures=[]
                for treasure in node["items"]:
                    class_treasure=get_class_by_name(treasure["class_name"])
                    
                    treasures.append({
                        "id":treasure["id"],
                        "is_selled":treasure["is_selled"],
                        "name":class_treasure.name,
                        "price":class_treasure.price,
                        "image_path":class_treasure.image_path,
                        "description":class_treasure.content,
                    })
                return {
                    "id":node["id"],
                    "name":node["name"],
                    "status":node["status"],
                    "shop_items":treasures
                }
            elif node["name"]=="event":
                event_class=get_class_by_name(node["event"])
                options = [
                    # {k: v for k, v in opt.items() if k != "function"}
                    # for opt in event_class.options
                ]
                for opt in event_class.options:
                    options.append({
                        "title":opt["title"],
                        "description":opt["description"],
                        "is_valid":opt["valid_check"](room_info),
                    })

                return {
                    "id":node["id"],
                    "name":node["name"],
                    "status":node["status"],
                    "title":event_class.title,
                    "image":event_class.image,
                    "description":event_class.description,
                    "options":options,
                }

    def treasure_to_json(self,treasures:list):
        treasures_json=[]
        for treasure in treasures:
            class_treasure=get_class_by_name(treasure)
            treasures_json.append({
                "name":class_treasure.name,
                "image_path":class_treasure.image_path,
                "description":class_treasure.content,
            })
        return treasures_json
    
    def get_node_by_id(self,map_structure:list,node_id:str):
        for layer in map_structure:
            for node in layer:
                if node["id"]==node_id:
                    return node
        return None

    def get_shop_item_by_id(self,shop_node:dict,item_id:str):
        for treasure in shop_node["items"]:
            if treasure["id"]==item_id:
                return treasure
        return None
        

    def get_next_node_layer(self,map_structure:list,node_id:str):
        for i_layer,layer in enumerate(map_structure):
            for i_node,node in enumerate(layer):
                if node["id"]==node_id and len(map_structure)>i_layer+1:
                    if len(map_structure[i_layer+1])==len(map_structure[i_layer]):
                        return [map_structure[i_layer+1][i_node]]
                    else:
                        return map_structure[i_layer+1]
            if i_layer==len(map_structure)-1:
                return []
        return None
    
    def get_current_layer(self,map_structure:list,node_id:str):
        for i,layer in enumerate(map_structure):
            for node in layer:
                if node["id"]==node_id:
                    return map_structure[i]
        return None

    def cards_to_json(self,cards:list):
        cards_json=[]
        for card in cards:
            card_class=CARD_DICTION[f"{card['name']}_{card['type_card']}"]
            player = SimpleNamespace()
            player.room = SimpleNamespace()
            player.room.stack = None
            player.room.get_flag=None
            card_obj=card_class(player)
            image=card_obj.image_path.replace("image.jpg","compress_img.jpg")
            result={
                "name":card["name"],
                "quantity":card["number"],
                "manaCost":card_obj.mana_cost,
                "type":card_obj.type_card,
                "image_path":image,
                "description":card_obj.content,
                "attack":0 if card_obj.type!="Creature" else card_obj.actual_power,
                "defense":0 if card_obj.type!="Creature" else card_obj.actual_live,
            }
            cards_json.append(result)
        return cards_json


    def room_progress(self,room:dict):
        level=room["map_detail"]["level"]
        if level==2:
            return (False,3)
        level+=1
        new_map_structure=self.create_map(level)
        return (True,level,new_map_structure)
        

    
    
    
        
if __name__=="__main__":
    import json
    rogue_manager=Rogue_Manager()
    map=rogue_manager.create_map(level=0)
    #print(map)
    print(json.dumps(rogue_manager.to_json(map),indent=4))
