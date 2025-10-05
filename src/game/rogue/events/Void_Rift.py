import random
import uuid

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event
from game.game_function_tool import ORGPATH



class Void_Rift(Base_Event):
    title="Void Rift"
    description='Before you lies a rift of pure darkness, tearing through the air. The void calls to you...'
    image="🌀"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 投掷石头 → 失去 5 生命
        player_profile["profile"]["max_life"] -= 5

    @classmethod
    def function_2(cls,player_profile:dict):
        # 绕开裂隙 → 什么都不发生
        pass

    @classmethod
    def function_3(cls,player_profile:dict):
        # 踏入裂隙 → 触发隐藏 Boss 战
        if player_profile["extra_info"].get("void_mark_1",False) and player_profile["extra_info"].get("void_mark_2",False):
            
            boss_detail={
                "id":str(uuid.uuid4()),
                "name":"battle",
                "status":"locked",
                "agent_name":"🌀",
                "agent_config":f"{ORGPATH}/game/rlearning/weights/boss/ppo_transformer.yaml",
                "agent_max_life":100,
                "agent_win_price":random.randint(40,80),
                "avatar":"🌀",
                "description":"🌀🌀🌀Having the treasure Mirror of Reflection and Cloak of the Shadow Thief , it is impossible to defeat.🌀🌀🌀",
                "treasures":[
                    "pytreasures.Mirror_of_Reflection.model.Mirror_of_Reflection",
                    "pytreasures.Cloak_of_the_Shadow_Thief.model.Cloak_of_the_Shadow_Thief",
                ],
            
            }
            player_profile["map_detail"]["map_structure"].append([boss_detail])
    @classmethod
    def cheak_valid_3(cls,player_profile:dict):
        return player_profile["extra_info"].get("void_mark_1",False) and player_profile["extra_info"].get("void_mark_2",False)

Void_Rift.options=[
    {
        "title": "Throw a Stone",
        "description": 'You hurl a stone into the rift. It recoils violently. Lose 5 HP.',
        "function": Void_Rift.function_1,
        "valid_check":Void_Rift.cheak_valid_1
    },
    {
        "title": "Avoid the Rift",
        "description": 'You decide it is too dangerous and leave. Nothing happens.',
        "function": Void_Rift.function_2,
        "valid_check":Void_Rift.cheak_valid_2
    },
    {
        "title": "Step into the Rift",
        "description": 'The void embraces you... (Hidden Boss Encounter)',
        "function": Void_Rift.function_3,
        "valid_check":Void_Rift.cheak_valid_3
    },
]
