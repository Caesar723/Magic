import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event





class Spirit_of_the_Bloom(Base_Event):
    title="Spirit of the Bloom"
    description='In a grove illuminated by soft light, a gentle flower spirit appears. She notices the withered bloom you carry, her eyes filled with longing and gratitude...'
    image="🧚‍♀️🌺"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 普通选项 → 与她交谈 → 获得 20 金币
        player_profile["profile"]["currency"] += 20

    @classmethod
    def function_2(cls,player_profile:dict):
        # 普通选项 → 接受祝福 → 回复 12 生命
        player_profile["profile"]["max_life"] += 12

    @classmethod
    def function_3(cls,player_profile:dict):
        # 联动选项（仅当有 flower_mark） → 归还花朵 → 获得专属宝藏【花之护符】
        if player_profile["extra_info"].get("flower_mark",False):
            treasure="pytreasures.Flower_Charm.model.Flower_Charm"
            player_profile["profile"]["treasures"].append(treasure)
            
    @classmethod
    def cheak_valid_3(cls,player_profile:dict):
        return player_profile["extra_info"].get("flower_mark",False)

Spirit_of_the_Bloom.options=[
    {
        "title": "Speak with Her",
        "description": 'You converse with the spirit. She leaves you a gift of coins. Gain 20 currency.',
        "function": Spirit_of_the_Bloom.function_1,
        "valid_check":Spirit_of_the_Bloom.cheak_valid_1
    },
    {
        "title": "Accept Her Blessing",
        "description": 'The spirit touches your forehead, filling you with warmth. Restore 12 health.',
        "function": Spirit_of_the_Bloom.function_2,
        "valid_check":Spirit_of_the_Bloom.cheak_valid_2
    },
    {
        "title": "Return the Bloom",
        "description": 'You return the withered flower. The spirit smiles, gifting you the legendary *Flower Charm*.',
        "function": Spirit_of_the_Bloom.function_3,
        "valid_check":Spirit_of_the_Bloom.cheak_valid_3
    },
]
