from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from game.base_agent_room import Base_Agent_Room
    from game.agent import Agent_Player as Agent
    from game.type_cards.creature import Creature











def get_reward(room:"Base_Agent_Room",agent:"Agent",battled_creature:"Creature"=None,attacker:"Creature"=None):#返回一个评分
    # if agent.life<=0:
    #     return -1
    # elif agent.opponent.life<=0:
    #     return 1
    self_live_reward=lambda x :x/5#lambda x :1/(1+np.e**(4-x))#用于红色的公式，卖血
    oppo_live_reward=lambda x :x/5

    score_life_self=self_live_reward(agent.life)
    score_oppo_self=oppo_live_reward(agent.opponent.life)

    score_battle_self_creatures=[room.get_creature_reward(card,battled_creature==card) for card in agent.battlefield]
    score_battle_self=sum(score_battle_self_creatures)
    
    
    score_battle_oppo_creatures=[room.get_creature_reward(card,card==attacker) for card in agent.opponent.battlefield]
    score_battle_oppo=sum(score_battle_oppo_creatures)

    # score_battle_self=sum(
    #     [
    #         self.get_creature_reward(card,battled_creature==card) for card in agent.battlefield
    #     ]
    # )#这个处以20表面随从不是很重要，重要的是敌方的血量
    
    # score_battle_oppo=sum(
    #     [
    #         self.get_creature_reward(card) for card in agent.opponent.battlefield
    #     ]
    # )

    score_mana=0
    for land in agent.land_area:
        score_mana+=sum(land.generate_mana().values())

    score_hand=len(agent.hand)/30
    score_mana=score_mana/20

    reward=score_hand+(score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo

    strength=3
    #print(agent.get_counter_from_dict("turn_count"))
    reward=reward/((agent.get_counter_from_dict("turn_count")+strength)/strength)
    result={
        "reward":reward,
        "score_life_self":score_life_self,
        "score_oppo_self":score_oppo_self,
        "score_mana":score_mana,
        "score_hand":score_hand,
        "score_battle_self":score_battle_self,
        "score_battle_oppo":score_battle_oppo,
        "score_battle_self_creatures":score_battle_self_creatures,
        "score_battle_oppo_creatures":score_battle_oppo_creatures
    }
    #print(score_life_self,score_oppo_self,score_mana,score_battle_self,score_battle_oppo)

    return result