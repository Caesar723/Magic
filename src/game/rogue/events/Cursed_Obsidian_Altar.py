import random

from game import treasure
from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event





class Cursed_Obsidian_Altar(Base_Event):
    title="Cursed Obsidian Altar"
    description='In the temple’s depths, you find a black altar carved from obsidian. A crimson flame flickers on top, and whispers echo in your mind, tempting you with forbidden power...'
    image="🪨🔥"

    @classmethod
    def function_1(cls,player_profile:dict):
        player_profile["profile"]["max_life"]+=3
        player_profile["profile"]["currency"]-=3

    @classmethod
    def function_2(cls,player_profile:dict):
        if random.random()<0.6:
            treasure=random.choice(ROGUE_TREASURE_DICT["low_level"]["treasure_list"])
            player_profile["profile"]["treasures"].append(treasure)
        else:
            player_profile["profile"]["max_life"]-=3

    @classmethod
    def function_3(cls,player_profile:dict):
        pass

Cursed_Obsidian_Altar.options=[
    {
        "title": "Make a Blood Offering",
        "description": 'Offer some of your wealth to the flame. Lose 3 currency, gain +3 max life.',
        "function": Cursed_Obsidian_Altar.function_1,
        "valid_check":Cursed_Obsidian_Altar.cheak_valid_1
    },
    {
        "title": "Grasp the Relic",
        "description": 'Seize the relic atop the altar. 60% chance to obtain *Cursed Relic*, 40% chance to suffer -3 health.',
        "function": Cursed_Obsidian_Altar.function_2,
        "valid_check":Cursed_Obsidian_Altar.cheak_valid_2
    },
    {
        "title": "Ignore the Temptation",
        "description": 'You resist the whispers and leave the altar untouched.',
        "function": Cursed_Obsidian_Altar.function_3,
        "valid_check":Cursed_Obsidian_Altar.cheak_valid_3
    },
]
