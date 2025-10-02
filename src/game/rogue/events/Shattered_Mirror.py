import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event




class Shattered_Mirror(Base_Event):
    title="Shattered Mirror"
    description='In the ruins you find a broken black mirror. Its fragments shimmer with unsettling darkness...'
    image="🪞"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 照一眼 → 回复 5 生命
        player_profile["profile"]["max_life"] += 5

    @classmethod
    def function_2(cls,player_profile:dict):
        # 捡起碎片 → 获得 15 金币
        player_profile["profile"]["currency"] += 15

    @classmethod
    def function_3(cls,player_profile:dict):
        # 触摸裂痕 → 获得虚空印记 void_mark_1
        player_profile["extra_info"]["void_mark_1"] = True

Shattered_Mirror.options=[
    {
        "title": "Look into the Shard",
        "description": 'You stare into the dark shard. Restore 5 health.',
        "function": Shattered_Mirror.function_1,
        "valid_check":Shattered_Mirror.cheak_valid_1
    },
    {
        "title": "Pick up a Fragment",
        "description": 'The shards glimmer faintly. Gain 15 currency.',
        "function": Shattered_Mirror.function_2,
        "valid_check":Shattered_Mirror.cheak_valid_2
    },
    {
        "title": "Touch the Crack",
        "description": 'A black glow burns into your hand... (You gain a hidden mark)',
        "function": Shattered_Mirror.function_3,
        "valid_check":Shattered_Mirror.cheak_valid_3
    },
]
