import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event






class Ancient_Throne(Base_Event):
    title="Ancient Throne"
    description='A shattered golden throne stands in the center of the hall. As you sit upon it, phantom subjects kneel before you, and the air grows heavy with forgotten authority.'
    image="👑"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 王之气魄 → 获得生命和金币
        player_profile["profile"]["max_life"]+=15
        player_profile["profile"]["currency"]+=15

    @classmethod
    def function_2(cls,player_profile:dict):
        # 王之遗产 → 获得 2 件强力宝藏
        
        for _ in range(2):
            treasure=random.choice(ROGUE_TREASURE_DICT["high_level"]["treasure_list"])
            player_profile["profile"]["treasures"].append(treasure)

    @classmethod
    def function_3(cls,player_profile:dict):
        # 王之威严 → Boss 血量 -20%
        last_node=player_profile["map_detail"]["map_structure"][-1]
        last_node=last_node[0]
        if last_node["name"]=="battle":
            last_node["agent_max_life"]=int(last_node["agent_max_life"]*0.8)
            
        

Ancient_Throne.options=[
    {
        "title": "King’s Might",
        "description": 'Gain +15 max life and +15 currency immediately.',
        "function": Ancient_Throne.function_1,
        "valid_check":Ancient_Throne.cheak_valid_1
    },
    {
        "title": "King’s Legacy",
        "description": 'Receive 2 powerful treasures from the phantom king’s vault.',
        "function": Ancient_Throne.function_2,
        "valid_check":Ancient_Throne.cheak_valid_2
    },
    {
        "title": "King’s Authority",
        "description": 'Your regal aura weakens the final enemy. The boss will have -20% max HP.',
        "function": Ancient_Throne.function_3,
        "valid_check":Ancient_Throne.cheak_valid_3
    },
]
