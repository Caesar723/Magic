import numpy as np
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.base_agent_room import Base_Agent_Room
    from game.agent import Agent_Player as Agent
    from game.type_cards.creature import Creature








"""
让状态归一
1-我方英雄的血量/20
1-敌方英雄的血量/20
蓝色，红色，绿色，白色，黑色法力值（通过计算地牌来得出）/10
卡牌(10):[编号，法力值]使用嵌入式（10*20）
    # 定义嵌入层
    # card_embedding = tf.keras.layers.Embedding(input_dim=100, output_dim=14)  # 卡牌编号的嵌入层
    (0,0,0,0,0,0)
    # hand_cards_embedded = tf.concat([
    #     card_embedding(hand_cards[:, 0]),
    #     mana_embedding(hand_cards[:, 1])
    # ], axis=-1)
我方场地(10):[攻击力，生命值]/10 , [1,0]是否可以攻击和防御
敌方场地(10):[攻击力，生命值]/10 , [1,0]是否可以攻击和防御
时间状态[0,1]:本回合，敌方攻击
攻击的随从[攻击力，生命值]/10
"""

def get_state(room:"Base_Agent_Room",agent:"Agent"):
    oppo_agent=agent.opponent

    self_life=1-agent.life/agent.ini_life
    oppo_life=1-oppo_agent.life/oppo_agent.ini_life

    lifes=np.array([self_life,oppo_life])

    cost=room.get_cost_total(agent)
    colors=np.array([cost["U"],cost["R"],cost["G"],cost["W"],cost["B"]])

    cards_hand_costs=[]
    length_hand=len(agent.hand)
    for hand_i in range(10):
        if hand_i <length_hand:
            card=agent.hand[hand_i]
            cards_hand_costs.append(list(card.calculate_cost().values()))
        else:
            cards_hand_costs.append([0,0,0,0,0,0])
    cards_hand_costs=np.array(cards_hand_costs)
    cards_hand_costs=cards_hand_costs.flatten()/10

    self_battlefield=get_creature_state(room,agent,agent.battlefield)
    oppo_battlefield=get_creature_state(room,agent,oppo_agent.battlefield)

    time_state=room.get_time_state()

    attacker=room.get_attacker()

    cards_id=[]
    for id_i in range(10):
        if id_i <length_hand:
            card=agent.hand[id_i]
            cards_id.append(agent.id_dict[f"{card.name}+{card.type}"])
        else:
            cards_id.append(0)

    cards_id=np.array(cards_id)
    
    num_state=np.concatenate((lifes,colors,cards_hand_costs,self_battlefield,oppo_battlefield,time_state,attacker))

    return num_state,cards_id


def get_creature_state(room,array:list[Creature]):
    length=len(array)
    result=[]
    for i in range(10):
        if i < length:
            activate=[0]
            if not array[i].get_flag("tap") and not array[i].get_flag("summoning_sickness"):
                activate=[10]
            result.append(list(array[i].state)+activate)
        else:
            result.append([0,0,0])
    result=np.array(result)
    result=result.flatten()/10
    return result
