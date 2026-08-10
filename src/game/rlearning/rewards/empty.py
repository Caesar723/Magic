from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from game.base_agent_room import Base_Agent_Room
    from game.agent import Agent_Player as Agent
    from game.type_cards.creature import Creature











def get_reward(room:"Base_Agent_Room",agent:"Agent",battled_creature:"Creature"=None,attacker:"Creature"=None):#返回一个评分

    result={
        "reward":0,
        "score_life_self":0,
        "score_oppo_self":0,
        "score_mana":0,
        "score_hand":0,
        "score_battle_self":0,
        "score_battle_oppo":0,
        "score_battle_self_creatures":0,
        "score_battle_oppo_creatures":0
    }

    return result