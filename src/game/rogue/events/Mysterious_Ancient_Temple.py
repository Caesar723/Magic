import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event

class Mysterious_Ancient_Temple(Base_Event):
    title="Mysterious Ancient Temple"
    description='Deep in the forest, you discover an ancient temple covered in vines. A faint blue glow emanates from its entrance, and the air is thick with ancient magic. Ancient runes carved on the stone door seem to whisper secrets of the past. You sense great power hidden here, but also unknown dangers...'
    image="🏛️"
    @classmethod
    def function_1(cls,player_profile:dict):
        player_profile["profile"]["currency"]+=5

    @classmethod
    def function_2(cls,player_profile:dict):
        if random.random()<0.5:
            level_dict=["low_level","middle_level","high_level"]
            level_key=player_profile["map_detail"]["level"]
            player_profile["profile"]["treasures"].append(random.choice(ROGUE_TREASURE_DICT[level_dict[level_key]]["treasure_list"]))
        else:
            player_profile["profile"]["max_life"]-=2

    @classmethod
    def function_3(cls,player_profile:dict):
        pass

    
Mysterious_Ancient_Temple.options=[
        {
            "title": "Cautious Exploration",
            "description": 'Carefully enter the temple, paying close attention to traps and clues. Gain 5 currency.',
            "function": Mysterious_Ancient_Temple.function_1,
            "valid_check":Mysterious_Ancient_Temple.cheak_valid_1
        },
        {
            "title": "Charge In",
            "description": 'Bravely rush deep into the temple, ignoring potential dangers. 50% chance to obtain treasure, 50% chance to trigger a trap(lose 2 health).',
            "function": Mysterious_Ancient_Temple.function_2,
            "valid_check":Mysterious_Ancient_Temple.cheak_valid_2
        },
        {
            "title": "Leave the Place",
            "description": 'Feeling it’s too dangerous, you decide to leave. You remain in your current state and gain no rewards.',
            "function": Mysterious_Ancient_Temple.function_3,
            "valid_check":Mysterious_Ancient_Temple.cheak_valid_3
        },
        
    ]
        
    