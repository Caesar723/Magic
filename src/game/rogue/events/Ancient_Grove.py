import random
from game.rogue.base_event import Base_Event
from game.rogue.rogue_dict import ROGUE_TREASURE_DICT


class Ancient_Grove(Base_Event):
    title = "Ancient Grove"
    description = (
        "An immense tree stands in the center of an untouched grove. "
        "Its bark glows faintly, covered in runes older than any known civilization."
    )
    image = "🌲"

    @classmethod
    def function_1(cls, player_profile: dict):
        # 「Feed your memories」→ 牺牲随机一个宝藏，换取 colossus_mark_2
        if player_profile["profile"]["treasures"]:
            lost_treasure = random.choice(player_profile["profile"]["treasures"])
            player_profile["profile"]["treasures"].remove(lost_treasure)
        player_profile["extra_info"]["colossus_mark_2"] = True

    @classmethod
    def function_2(cls, player_profile: dict):
        # 「Let your blood flow into the roots」→ 失去 15 HP，获得 1 个“活着的”宝藏（随机特殊）
        player_profile["profile"]["max_life"] = max(1, player_profile["profile"]["max_life"] - 15)
        living_treasure = random.choice([
            "pytreasures.Void_Scepter.model.Void_Scepter",
            "pytreasures.Flower_Charm.model.Flower_Charm",
            "pytreasures.Sun_Ring.model.Sun_Ring"
        ])
        player_profile["profile"]["treasures"].append(living_treasure)


    @classmethod
    def function_3(cls, player_profile: dict):
        # 离开 → 无事发生
        new_treasure = random.choice(ROGUE_TREASURE_DICT["low_level"]["treasure_list"])
        player_profile["profile"]["treasures"].append(new_treasure)

    @classmethod
    def check_valid_1(cls, player_profile: dict):
        return bool(player_profile["profile"]["treasures"])

    @classmethod
    def check_valid_2(cls, player_profile: dict):
        return player_profile["profile"]["max_life"] > 15

    @classmethod
    def check_valid_3(cls, player_profile: dict):
        return True


Ancient_Grove.options = [
    {
        "title": "Feed Your Memories",
        "description": "You press your hand against the trunk. It demands something precious. (Lose 1 random treasure, gain Colossus Mark II)",
        "function": Ancient_Grove.function_1,
        "valid_check": Ancient_Grove.check_valid_1,
    },
    {
        "title": "Let Your Blood Flow into the Roots",
        "description": "You drive your hand into the soil, letting the roots drink your blood. They pulse... something within awakens. (-15 HP, gain 1 living treasure)",
        "function": Ancient_Grove.function_2,
        "valid_check": Ancient_Grove.check_valid_2,
    },
    {
        "title": "Listen to the Forest’s Voice",
        "description": "You lean close to the bark. The whispers are soft... and sharp. (-10 HP, gain 1 low-level treasure)",
        "function": Ancient_Grove.function_3,
        "valid_check": Ancient_Grove.check_valid_3,
    }
]
