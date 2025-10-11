import random
from game.rogue.base_event import Base_Event
from game.rogue.rogue_dict import ROGUE_TREASURE_DICT

class Whispering_Roots(Base_Event):
    title = "Whispering Roots"
    description = (
        "Thick roots twist from the ground, pulsing faintly with green light. "
        "A whisper runs through the earth as if something below is listening."
    )
    image = "🌿"

    @classmethod
    def function_1(cls, player_profile: dict):
        # 触摸树根 → 受伤，获得 colossus_mark_1
        player_profile["profile"]["max_life"] = max(0, player_profile["profile"]["max_life"] - 10)
        player_profile["extra_info"]["colossus_mark_1"] = True

    @classmethod
    def function_2(cls, player_profile: dict):
        # 拔出一根树根 → 被自然反噬
        player_profile["profile"]["max_life"] = max(1, player_profile["profile"]["max_life"] - 5)
        treasure=random.choice(ROGUE_TREASURE_DICT["high_level"]["treasure_list"])
        player_profile["profile"]["treasures"].append(treasure)

    @classmethod
    def function_3(cls, player_profile: dict):
        # 离开 → 无事发生
        pass

    @classmethod
    def check_valid_1(cls, player_profile: dict):
        return player_profile["profile"]["max_life"] > 10

    @classmethod
    def check_valid_2(cls, player_profile: dict):
        return player_profile["profile"]["max_life"] > 5

    


Whispering_Roots.options = [
    {
        "title": "Touch the Roots",
        "description": "You reach out — green light seeps into your skin. It burns like sap turned to fire. (-10 HP, Gain Colossus Mark I)",
        "function": Whispering_Roots.function_1,
        "valid_check": Whispering_Roots.check_valid_1,
    },
    {
        "title": "Pull a Root Free",
        "description": "You tear one from the earth. It screams in your mind (-5 Max HP) but you find a treasure. ",
        "function": Whispering_Roots.function_2,
        "valid_check": Whispering_Roots.check_valid_2,
    },
    {
        "title": "Leave Quietly",
        "description": "You decide not to disturb the forest’s whispers.",
        "function": Whispering_Roots.function_3,
        "valid_check": Whispering_Roots.cheak_valid_3,
    },
]
