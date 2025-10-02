import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event





class Cursed_Inscription(Base_Event):
    title="Cursed Inscription"
    description='The wall glows with ancient runes. As you draw closer, the characters twist and burn into your vision. You feel an unavoidable curse creeping in…'
    image="📜🩸"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 失去 10 点最大生命
        player_profile["profile"]["max_life"]-=10

    @classmethod
    def function_2(cls,player_profile:dict):
        # 随机失去一个宝藏，并交给 boss
        if player_profile["profile"]["treasures"]:
            lost_treasure=random.choice(player_profile["profile"]["treasures"])
            player_profile["profile"]["treasures"].remove(lost_treasure)
            boss_node=player_profile["map_detail"]["map_structure"][-1][0]
            boss_node["treasures"].append(lost_treasure)

    @classmethod
    def function_3(cls,player_profile:dict):
        # 这一层之后遇到的怪物最大生命 +10
        current_flag=False
        for node in player_profile["map_detail"]["map_structure"]:
            for node_ in node:
                if node_["status"]=="current":
                    current_flag=True
                    continue
                if current_flag and node_["name"]=="battle":
                    node_["agent_max_life"]+=10
                    

Cursed_Inscription.options=[
    {
        "title": "Accept the Rune’s Brand",
        "description": 'The curse sears into your soul. Lose **10 max life**.',
        "function": Cursed_Inscription.function_1,
        "valid_check":Cursed_Inscription.cheak_valid_1
    },
    {
        "title": "Sacrifice a Treasure",
        "description": 'The rune demands an offering. Lose **1 random treasure** (it empowers the boss).',
        "function": Cursed_Inscription.function_2,
        "valid_check":Cursed_Inscription.cheak_valid_2
    },
    {
        "title": "Spread the Curse",
        "description": 'The runes leak power into the dungeon. All enemies on this floor gain **+10 max life**.',
        "function": Cursed_Inscription.function_3,
        "valid_check":Cursed_Inscription.cheak_valid_3
    },
]
