
import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event





class Whispering_Tome(Base_Event):
    title="Whispering Tome"
    description='A dusty tome whispers as you flip its pages. Its voice beckons you to listen...'
    image="📖"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 阅读一页 → 获得普通宝藏
        treasure = random.choice(ROGUE_TREASURE_DICT["low_level"]["treasure_list"])
        player_profile["profile"]["treasures"].append(treasure)

    @classmethod
    def function_2(cls,player_profile:dict):
        # 合上书本 → 回复 10 生命
        player_profile["profile"]["max_life"] += 10

    @classmethod
    def function_3(cls,player_profile:dict):
        # 献出鲜血 → 失去 5 生命，获得虚空印记 void_mark_2
        player_profile["profile"]["max_life"] -= 5
        
        player_profile["extra_info"]["void_mark_2"] = True


    @classmethod
    def cheak_valid_3(cls,player_profile:dict):
        return player_profile["profile"]["max_life"] > 5

Whispering_Tome.options=[
    {
        "title": "Read a Page",
        "description": 'You skim the forbidden text. Gain 1 common treasure.',
        "function": Whispering_Tome.function_1,
        "valid_check":Whispering_Tome.cheak_valid_1
    },
    {
        "title": "Close the Tome",
        "description": 'You push the whispers away. Restore 10 health.',
        "function": Whispering_Tome.function_2,
        "valid_check":Whispering_Tome.cheak_valid_2
    },
    {
        "title": "Offer Blood",
        "description": 'Your blood seeps into the pages. Lose 5 HP. (You gain a hidden mark)',
        "function": Whispering_Tome.function_3,
        "valid_check":Whispering_Tome.cheak_valid_3
    },
]
