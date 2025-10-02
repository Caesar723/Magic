import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event






class Forgotten_Pact(Base_Event):
    title="Forgotten Pact"
    description='A blood-stained contract floats before you, written in an ancient tongue. Your hand trembles, compelled to sign... Whatever you choose, a heavy price must be paid.'
    image="📜🩸"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 获得一个随机宝物，但金币获取率减半
        level_dict=["low_level","middle_level","high_level"]
        level_key=player_profile["map_detail"]["level"]
        new_treasure=random.choice(ROGUE_TREASURE_DICT[level_dict[level_key]]["treasure_list"])
        player_profile["profile"]["treasures"].append(new_treasure)
        # 设置金币获取率减半（假设用一个倍率字段控制）
        
        for node in player_profile["map_detail"]["map_structure"]:
            for node_ in node:
                if node_["name"]=="battle":
                    node_["agent_win_price"]=0
                    

    @classmethod
    def function_2(cls,player_profile:dict):
        # Boss 获得一件额外宝藏（从同级别池子里抽取）

        boss_treasure=random.choice(ROGUE_TREASURE_DICT["high_level"]["treasure_list"])
        player_profile["map_detail"]["map_structure"][-1][0]["treasures"].append(boss_treasure)

    @classmethod
    def function_3(cls,player_profile:dict):
        # 立刻失去 11 点生命
        player_profile["profile"]["life"]-=11

Forgotten_Pact.options=[
    {
        "title": "Sign with Blood",
        "description": 'Gain a random treasure, but your gold income is 0.',
        "function": Forgotten_Pact.function_1,
        "valid_check":Forgotten_Pact.cheak_valid_1
    },
    {
        "title": "Deliver to the Boss",
        "description": 'The contract vanishes into the dark. The boss gains an extra treasure.',
        "function": Forgotten_Pact.function_2,
        "valid_check":Forgotten_Pact.cheak_valid_2
    },
    {
        "title": "Resist the Temptation",
        "description": 'The contract burns your flesh as you resist. Lose 11 life.',
        "function": Forgotten_Pact.function_3,
        "valid_check":Forgotten_Pact.cheak_valid_3
    },
]
