import random
import uuid

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event
from game.game_function_tool import ORGPATH


class Emerald_Colossus(Base_Event):
    title = "Emerald Colossus"
    description = (
        "Covered in vines and moss, a colossal statue towers before you. "
        "Its eyes glow faint green, and ancient runes pulse faintly across its stone surface."
    )
    image = "🌑"

    @classmethod
    def function_1(cls, player_profile: dict):
        # 触摸巨像 → 世界被改变：所有怪物获得“Boots_of_the_Time_Traveler”
        current_flag=False
        for node in player_profile["map_detail"]["map_structure"]:
            for node_ in node:
                if node_["status"]=="current":
                    current_flag=True
                    continue
                if current_flag and node_["name"]=="battle":
                    node_["treasures"].append("pytreasures.Boots_of_the_Time_Traveler.model.Boots_of_the_Time_Traveler")
    @classmethod
    def function_2(cls, player_profile: dict):
        # 献血仪式 → 失去 20 生命，获得两个随机宝藏
        player_profile["profile"]["max_life"] = max(1, player_profile["profile"]["max_life"] - 20)
        
        for _ in range(2):
            new_treasure=random.choice(ROGUE_TREASURE_DICT["high_level"]["treasure_list"])
            player_profile["profile"]["treasures"].append(new_treasure)
        

    @classmethod
    def function_3(cls, player_profile: dict):
        # 触发隐藏Boss战
        if (
            player_profile["extra_info"].get("colossus_mark_1", False)
            and player_profile["extra_info"].get("colossus_mark_2", False)
        ):
            boss_detail = {
                "id": str(uuid.uuid4()),
                "name": "battle",
                "status": "locked",
                "agent_name": "🌑 The Emerald Sentinel",
                "agent_config": f"{ORGPATH}/game/rlearning/weights/growing/ppo_lstm8.yaml",
                "agent_max_life": 70,
                "agent_win_price": random.randint(80, 120),
                "avatar": "🌑",
                "description": (
                    "Forged from ancient stone and bound by the green lifeblood of the world, "
                    "the Emerald Sentinel guards what remains of the old gods. "
                    "It awakens only to those tainted by the void."
                ),
                "treasures": [
                    "pytreasures.Lucky_Clover_Pin.model.Lucky_Clover_Pin",
                    "pytreasures.Endless_Grimoire.model.Endless_Grimoire",
                ],
            }
            player_profile["map_detail"]["map_structure"].append([boss_detail])

    # ======== 可用性检查 ========
    @classmethod
    def check_valid_1(cls, player_profile: dict):
        return True

    @classmethod
    def check_valid_2(cls, player_profile: dict):
        return player_profile["profile"]["max_life"] > 20

    @classmethod
    def check_valid_3(cls, player_profile: dict):
        return (
            player_profile["extra_info"].get("colossus_mark_1", False)
            and player_profile["extra_info"].get("colossus_mark_2", False)
        )


Emerald_Colossus.options = [
    {
        "title": "Touch the Colossus",
        "description": "You touch the glowing moss — the world shudders. Every creature feels the pulse. (All future enemies gain Boots of the Time Traveler)",
        "function": Emerald_Colossus.function_1,
        "valid_check": Emerald_Colossus.check_valid_1,
    },
    {
        "title": "Offer Blood to the Stone",
        "description": "You carve your palm and let your blood flow into the cracks. The statue accepts your offering. (-20 HP, Gain 2 random treasures)",
        "function": Emerald_Colossus.function_2,
        "valid_check": Emerald_Colossus.check_valid_2,
    },
    {
        "title": "Stare into its Eyes",
        "description": "A faint hum echoes through the valley... The colossus awakens. (Hidden Boss Encounter)",
        "function": Emerald_Colossus.function_3,
        "valid_check": Emerald_Colossus.check_valid_3,
    },
]
