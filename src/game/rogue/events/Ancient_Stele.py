import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event




class Ancient_Stele(Base_Event):
    title="Ancient Stele"
    description='Inside the temple, you discover a stone stele covered in mysterious runes. The markings seem to glow faintly as you approach...'
    image="🗿"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 抄录符文 → 获得 10 金币
        player_profile["profile"]["currency"] += 10

    @classmethod
    def function_2(cls,player_profile:dict):
        # 触摸石碑 → 回复 5 点生命
        player_profile["profile"]["max_life"] += 5

    @classmethod
    def function_3(cls,player_profile:dict):
        # 刻下名字 → 获得标记 stele_mark
        player_profile["extra_info"]["stele_mark"] = True
        

Ancient_Stele.options=[
    {
        "title": "Copy the Runes",
        "description": 'You carefully copy down the ancient runes. Gain 10 currency.',
        "function": Ancient_Stele.function_1,
        "valid_check":Ancient_Stele.cheak_valid_1
    },
    {
        "title": "Touch the Stele",
        "description": 'The stone feels warm and soothing. Restore 5 health.',
        "function": Ancient_Stele.function_2,
        "valid_check":Ancient_Stele.cheak_valid_2
    },
    {
        "title": "Carve Your Name",
        "description": 'You carve your name into the stone, leaving a mark on history...',
        "function": Ancient_Stele.function_3,
        "valid_check":Ancient_Stele.cheak_valid_3
    },
]
