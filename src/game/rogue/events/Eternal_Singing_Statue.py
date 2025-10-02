import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event




class Eternal_Singing_Statue(Base_Event):
    title="Eternal Singing Statue"
    description='A stone statue of a long-forgotten goddess hums with eternal song. Its melody soothes your soul, but the tune carries strange distortions, as if luring you into dreams...'
    image="🎶🗿"

    @classmethod
    def function_1(cls,player_profile:dict):
        player_profile["profile"]["max_life"]+=4

    @classmethod
    def function_2(cls,player_profile:dict):
        if random.random()<0.5:
            treasure=random.choice(ROGUE_TREASURE_DICT["low_level"]["treasure_list"])
            player_profile["profile"]["treasures"].append(treasure)
        else:
            player_profile["profile"]["max_life"]-=1

    @classmethod
    def function_3(cls,player_profile:dict):
        player_profile["profile"]["currency"]+=2

Eternal_Singing_Statue.options=[
    {
        "title": "Listen Quietly",
        "description": 'You close your eyes and let the song heal your spirit. Restore 4 health.',
        "function": Eternal_Singing_Statue.function_1,
        "valid_check":Eternal_Singing_Statue.cheak_valid_1
    },
    {
        "title": "Sing Along",
        "description": 'Join the melody. 50% chance to obtain *Harmony Gem*, 50% chance to weaken yourself (-1 max life).',
        "function": Eternal_Singing_Statue.function_2,
        "valid_check":Eternal_Singing_Statue.cheak_valid_2
    },
    {
        "title": "Steal an Offering",
        "description": 'Search beneath the statue for offerings. Gain 2 currency.',
        "function": Eternal_Singing_Statue.function_3,
        "valid_check":Eternal_Singing_Statue.cheak_valid_3
    },
]
