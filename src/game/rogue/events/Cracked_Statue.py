import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event




class Cracked_Statue(Base_Event):
    title="Cracked Statue"
    description='An ancient statue stands before you, its surface marked with cracks. Something seems to be hidden within the stone...'
    image="🗿"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 掰开裂缝 → 获得普通宝藏，失去 3 点生命
        treasure=random.choice(ROGUE_TREASURE_DICT["low_level"]["treasure_list"])
        player_profile["profile"]["treasures"].append(treasure)
        player_profile["profile"]["max_life"]-=3

    @classmethod
    def function_2(cls,player_profile:dict):
        # 低声祈祷 → 回复 3 点生命
        player_profile["profile"]["max_life"]+=3

    @classmethod
    def function_3(cls,player_profile:dict):
        # 绕过 → 什么都不发生
        pass

Cracked_Statue.options=[
    {
        "title": "Break the Crack",
        "description": 'Force the statue open. Gain 1 common treasure but lose 3 health.',
        "function": Cracked_Statue.function_1,
        "valid_check":Cracked_Statue.cheak_valid_1
    },
    {
        "title": "Pray Softly",
        "description": 'You kneel and whisper a prayer. Restore 3 health.',
        "function": Cracked_Statue.function_2,
        "valid_check":Cracked_Statue.cheak_valid_2
    },
    {
        "title": "Walk Away",
        "description": 'You decide not to meddle with the statue and move on. Nothing happens.',
        "function": Cracked_Statue.function_3,
        "valid_check":Cracked_Statue.cheak_valid_3
    },
]
