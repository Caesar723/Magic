import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event





class Whispering_Flame(Base_Event):
    title="Whispering Flame"
    description='A lone eternal flame flickers on the wall, whispering faintly as if offering bargains to those who dare respond...'
    image="🕯️"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 用生命交换 → 失去 5 点生命，获得 1 件稀有宝藏
        player_profile["profile"]["max_life"] -= 5
        treasure = random.choice(ROGUE_TREASURE_DICT["high_level"]["treasure_list"])
        player_profile["profile"]["treasures"].append(treasure)

    @classmethod
    def function_2(cls,player_profile:dict):
        # 用金币交换 → 失去 20 金币，获得 1 件普通宝藏
        player_profile["profile"]["currency"] -= 20
        treasure = random.choice(ROGUE_TREASURE_DICT["low_level"]["treasure_list"])
        player_profile["profile"]["treasures"].append(treasure)

    @classmethod
    def function_3(cls,player_profile:dict):
        # 点燃自己 → 回复 12 点生命
        player_profile["profile"]["max_life"] += 12

    @classmethod
    def cheak_valid_1(cls,player_profile:dict):
        return player_profile["profile"]["max_life"] > 5

    @classmethod
    def cheak_valid_2(cls,player_profile:dict):
        return player_profile["profile"]["currency"] > 20

Whispering_Flame.options=[
    {
        "title": "Trade Blood",
        "description": 'Offer your life essence. Lose 5 HP, gain 1 rare treasure.',
        "function": Whispering_Flame.function_1,
        "valid_check":Whispering_Flame.cheak_valid_1
    },
    {
        "title": "Trade Gold",
        "description": 'Feed the flame with wealth. Lose 20 currency, gain 1 common treasure.',
        "function": Whispering_Flame.function_2,
        "valid_check":Whispering_Flame.cheak_valid_2
    },
    {
        "title": "Embrace the Flame",
        "description": 'Let the fire wash over you. Restore 12 health.',
        "function": Whispering_Flame.function_3,
        "valid_check":Whispering_Flame.cheak_valid_3
    },
]