import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event


class Altar_of_the_Burning_Sun(Base_Event):
    title="Altar of the Burning Sun"
    description='Through the shattered roof, blazing sunlight pours down upon a golden altar. You feel the overwhelming power of the sun blessing you with divine strength.'
    image="☀️"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 炽日遗产 → 获得宝藏【太阳指环】，永久减少所有伤害 -1
        treasure="pytreasures.Sun_Ring.model.Sun_Ring"
        player_profile["profile"]["treasures"].append(treasure)
        

    @classmethod
    def function_2(cls,player_profile:dict):
        # 太阳之恩 → 下一个敌人的生命为 5 点

        current_flag=False
        for node in player_profile["map_detail"]["map_structure"]:
            for node_ in node:
                if node_["status"]=="current":
                    current_flag=True
                    continue
                if current_flag and node_["name"]=="battle":
                    node_["agent_max_life"]=5
                    return
        
        

    @classmethod
    def function_3(cls,player_profile:dict):
        # 炽日财富 → 获得 50 金币
        player_profile["profile"]["currency"]+=50

Altar_of_the_Burning_Sun.options=[
    {
        "title": "Sun Ring",
        "description": 'Gain the exclusive treasure *Sun Ring*. Permanently reduce all incoming damage by half.',
        "function": Altar_of_the_Burning_Sun.function_1,
        "valid_check":Altar_of_the_Burning_Sun.cheak_valid_1
    },
    {
        "title": "Blessing of the Sun",
        "description": 'The sun’s wrath strikes your foes. At the start of your next battle, the enemy’s life is 5.',
        "function": Altar_of_the_Burning_Sun.function_2,
        "valid_check":Altar_of_the_Burning_Sun.cheak_valid_2
    },
    {
        "title": "Sun’s Wealth",
        "description": 'Golden light fills your purse. Gain 50 currency.',
        "function": Altar_of_the_Burning_Sun.function_3,
        "valid_check":Altar_of_the_Burning_Sun.cheak_valid_3
    },
]
