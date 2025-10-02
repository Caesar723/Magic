import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event






class Poisoned_Darts_Trap(Base_Event):
    title="Poisoned Darts Trap"
    description='As you step into the corridor, hidden mechanisms activate. From the walls, countless poisoned darts shoot out! There is no way to avoid harm—you must react quickly...'
    image="🏹☠️"

    @classmethod
    def function_1(cls,player_profile:dict):
        if player_profile["profile"]["treasures"]:
            lost_treasure=random.choice(player_profile["profile"]["treasures"])
            player_profile["profile"]["treasures"].remove(lost_treasure)

    @classmethod
    def function_2(cls,player_profile:dict):
        player_profile["profile"]["max_life"]-=2

    @classmethod
    def function_3(cls,player_profile:dict):
        player_profile["profile"]["currency"]-=5

Poisoned_Darts_Trap.options=[
    {
        "title": "Shield Yourself",
        "description": 'You block with your arm, loss one treasure.',
        "function": Poisoned_Darts_Trap.function_1,
        "valid_check":Poisoned_Darts_Trap.cheak_valid_1
    },
    {
        "title": "Dodge Recklessly",
        "description": 'You avoid most darts, but strain yourself. Lose -2 max life.',
        "function": Poisoned_Darts_Trap.function_2,
        "valid_check":Poisoned_Darts_Trap.cheak_valid_2
    },
    {
        "title": "Use Currency as Distraction",
        "description": 'You throw coins to jam the trap. Lose 5 currency.',
        "function": Poisoned_Darts_Trap.function_3,
        "valid_check":Poisoned_Darts_Trap.cheak_valid_3
    },
]
