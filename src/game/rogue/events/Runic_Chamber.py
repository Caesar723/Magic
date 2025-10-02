import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event


class Runic_Chamber(Base_Event):
    title="Runic Chamber"
    description='You stumble upon a hidden chamber. The walls are covered with the same runes you saw before. The air hums with ancient magic...'
    image="🔮"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 普通选项 → 搜索 → 获得 20 金币
        player_profile["profile"]["currency"] += 20

    @classmethod
    def function_2(cls,player_profile:dict):
        # 普通选项 → 冥想 → 回复 8 生命
        player_profile["profile"]["max_life"] += 8

    @classmethod
    def function_3(cls,player_profile:dict):
        # 联动选项（仅当有 stele_mark） → 解读石碑 → 获得2件稀有宝藏
        if player_profile["extra_info"].get("stele_mark",False):
            treasure = random.choice(ROGUE_TREASURE_DICT["high_level"]["treasure_list"])
            player_profile["profile"]["treasures"].append(treasure)
            treasure = random.choice(ROGUE_TREASURE_DICT["high_level"]["treasure_list"])
            player_profile["profile"]["treasures"].append(treasure)

    @classmethod
    def cheak_valid_3(cls,player_profile:dict):
        return player_profile["extra_info"].get("stele_mark",False)

Runic_Chamber.options=[
    {
        "title": "Search the Chamber",
        "description": 'You find scattered coins and offerings. Gain 20 currency.',
        "function": Runic_Chamber.function_1,
        "valid_check":Runic_Chamber.cheak_valid_1
    },
    {
        "title": "Meditate Among the Runes",
        "description": 'You sit and let the runes soothe your soul. Restore 8 health.',
        "function": Runic_Chamber.function_2,
        "valid_check":Runic_Chamber.cheak_valid_2
    },
    {
        "title": "Interpret the Stele",
        "description": 'Because you carved your name on the ancient stele, the runes resonate. Gain 2 rare treasures.',
        "function": Runic_Chamber.function_3,
        "valid_check":Runic_Chamber.cheak_valid_3
    },
]
