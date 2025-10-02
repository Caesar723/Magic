import random

from game.rogue.rogue_dict import ROGUE_TREASURE_DICT
from game.rogue.base_event import Base_Event






class Stellar_Altar(Base_Event):
    title="Stellar Altar"
    description='In the center of the hall, a jewel-encrusted altar shines with starlight. As the cosmic glow lifts your body, you feel the universe itself offering you a gift...'
    image="🌌"

    @classmethod
    def function_1(cls,player_profile:dict):
        # 星之护佑 → 永久 +20 最大生命
        player_profile["profile"]["max_life"]+=20

    @classmethod
    def function_2(cls,player_profile:dict):
        # 星之馈赠 → 固定获得专属宝藏：虚空权杖
        void_scepter = "pytreasures.Void_Scepter.model.Void_Scepter"
        player_profile["profile"]["treasures"].append(void_scepter)

    @classmethod
    def function_3(cls,player_profile:dict):
        # 星之财富 → 获得 100 金币
        player_profile["profile"]["currency"]+=100

Stellar_Altar.options=[
    {
        "title": "Starlight’s Protection",
        "description": 'The cosmic blessing strengthens your body. Gain +20 max life.',
        "function": Stellar_Altar.function_1,
        "valid_check":Stellar_Altar.cheak_valid_1
    },
    {
        "title": "Gift of the Stars",
        "description": 'The altar grants you a relic of pure void. Gain the exclusive treasure *Void Scepter*.',
        "function": Stellar_Altar.function_2,
        "valid_check":Stellar_Altar.cheak_valid_2
    },
    {
        "title": "Wealth of the Cosmos",
        "description": 'Golden stardust rains upon you. Gain 100 currency.',
        "function": Stellar_Altar.function_3,
        "valid_check":Stellar_Altar.cheak_valid_3
    },
]
