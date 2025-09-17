import asyncio
import aiofiles
from datetime import datetime
import os
import json, zlib
import time

import typing
if typing.TYPE_CHECKING:
    from game.player import Player
    from game.room import Room

from initinal_file import ORGPATH




class GameRecorder:
    def __init__(self,player:"Player",room:"Room",start_record:bool=True):
        self.game_room=room
        self.game_player=player
        if start_record:
            self.reset_save_flag()
        else:
            self.save_flag=True

        
        

    def reset_save_flag(self):
        self.save_flag=False
        self.datas=[]
        self.check_point_datas=[]
        
        self.start_time=time.perf_counter()

    async def store_game_message(self,message):
        #print(self.save_flag,message)
        if self.save_flag:
            return
        data={
            "game_records":message,
            #"game_ini_records":self.game_room.text(self.game_player),
            "game_times":time.perf_counter()-self.start_time
        }
        self.datas.append(data)
        self.start_time=time.perf_counter()

    async def store_game_ini_message(self,info):
        if self.save_flag:
            return
        data={
            "game_ini_records":self.game_room.text(self.game_player),
            "event_info":info,
            "index":len(self.datas)
        }
        self.check_point_datas.append(data)

    def message_to_binary(self):
        
        result={
            "basic_info":{
                "self_name":self.game_player.name,
                "opponent_name":self.game_player.opponent.name,
                
            },
            "game_records":self.datas,
            "check_point_datas":self.check_point_datas,
        }
        binary_data = json.dumps(result, ensure_ascii=False).encode("utf-8")
        binary_data = zlib.compress(binary_data)
        return binary_data

    async def save_binary(self):
        if self.save_flag:
            return
        self.save_flag=True
        now = datetime.now()
        time_str = now.strftime("%Y_%m_%d_%H_%M_%S")
        self_name=self.game_player.name
        opponent_name=self.game_player.opponent.name

        
        os.makedirs(f"{ORGPATH}/game/game_records/{self_name}",exist_ok=True)
        filename=f"{ORGPATH}/game/game_records/{self_name}/{self_name}_{opponent_name}_{time_str}.mgf"

        async with aiofiles.open(filename, "wb") as f:
            await f.write(self.message_to_binary())

        self.datas=[]
        self.check_point_datas=[]

if __name__=="__main__":
    import zlib
    file_path=f"/Users/xuanpeichen/Desktop/code/python/openai/src/game/game_records/Agent1_AgentCompanion_2025_09_16_14_43_23.bin"
    with open(file_path, "rb") as f:
        binary_data = f.read()
        data = zlib.decompress(binary_data)
        pairs = json.loads(data.decode("utf-8"))
    print(pairs[0][0])
    #print(zlib.compress(binary_data))
    #print(zlib.decompress(zlib.compress(binary_data)))