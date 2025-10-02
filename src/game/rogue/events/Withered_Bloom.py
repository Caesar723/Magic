import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event





class Withered_Bloom(Base_Event):
    title="Withered Bloom"
    description='In a corner of the ruins, you discover a withered flower, fragile and almost lifeless. It feels oddly significant...'
    image="🌸"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 丢弃 → 什么都不发生
        pass

    @classmethod
    def function_2(cls,player_profile:dict):
        # 压在书里 → 回复 5 点生命
        player_profile["profile"]["max_life"] += 5

    @classmethod
    def function_3(cls,player_profile:dict):
        # 小心保存 → 获得标记 flower_mark
        player_profile["extra_info"]["flower_mark"] = True

Withered_Bloom.options=[
    {
        "title": "Discard",
        "description": 'You toss the flower aside. Nothing happens.',
        "function": Withered_Bloom.function_1,
        "valid_check":Withered_Bloom.cheak_valid_1
    },
    {
        "title": "Press into a Book",
        "description": 'You carefully press the flower into your journal. Restore 5 health.',
        "function": Withered_Bloom.function_2,
        "valid_check":Withered_Bloom.cheak_valid_2
    },
    {
        "title": "Keep it Safe",
        "description": 'You tuck the fragile bloom away. Something about it feels important...',
        "function": Withered_Bloom.function_3,
        "valid_check":Withered_Bloom.cheak_valid_3
    },
]
