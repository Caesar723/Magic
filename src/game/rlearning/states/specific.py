
import numpy as np
from typing import TYPE_CHECKING

from game.rlearning.utils.model import get_class_by_name

if TYPE_CHECKING:
    from game.base_agent_room import Base_Agent_Room
    from game.agent import Agent_Player as Agent
    from game.type_cards.creature import Creature
    from game.type_cards.instant import Instant
    from game.type_cards.land import Land
    from game.type_cards.sorcery import Sorcery
    from game.card import Card


"""

state = {

    # ================= Hero =================

    "self_life": (21,),  # 我方英雄血量 one-hot [0,20]
    # example: hp=19 -> [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]

    "oppo_life": (21,),  # 敌方英雄血量 one-hot [0,20]
    # example: hp=19 -> [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]


    # ================= Mana =================

    "self_mana": [green, blue, red, white, black],
    # 五色法力，均使用 21-dim one-hot
    # example:
    # green=0 -> [1,0,0,...]
    # blue=20 -> [0,0,...,1]


    # ================= Action =================

    "action_history": [],  # 历史动作序列
    # example: [0]


    # ================= Hand =================

    "card_hand": {

        "card_types": (10,),             # 卡牌类型(nn.embedding)
        # example: [4,4,1,2,2,0,0,0,0,0]

        "card_special_types": (10,20),  # 特殊能力 multi-hot
        # example: [1,0,0,0,0,0,0,0,1,0,...]
        # => battlecry + summoning_sickness

        "card_costs": (10,6),
        # [colorless, green, blue, red, white, black]
        # 每个费用使用 21-dim one-hot
        # example: [5,1,0,0,0,0]
        # => colorless=5, green=1

        "card_atks": (10,),        # atk
        # example: [0,0,2,0,0,0,0,0,0,0]

        "card_hps": (10,),         # hp
        # example: [0,0,3,0,0,0,0,0,0,0]

        "card_has_attack": (10,),  # 是否可攻击 (0/1)
        # example: [0,0,1,0,0,0,0,0,0,0]

        "card_has_defend": (10,),  # 是否可防御 (0/1)
        # example: [0,0,1,0,0,0,0,0,0,0]

        "card_mask": (10,),        # 是否存在卡牌 (1=存在,0=padding)
        # example: [1,1,1,1,1,0,0,0,0,0]
    },


    # ================= Self Board =================

    "self_board": {

        "card_special_types": (10,20),  # 特殊能力 multi-hot

        "card_atks": (10,),             # atk
        # example: [2,4,0,0,0,0,0,0,0,0]

        "card_hps": (10,),              # hp

        "card_has_attack": (10,),       # 是否可攻击 (0/1)

        "card_has_defend": (10,),       # 是否可防御 (0/1)

        "card_mask": (10,)              # 是否存在随从
    },


    # ================= Opponent Board =================

    "oppo_board": {  # 与 self_board 完全一致

        "card_special_types": (10,20),
        "card_atks": (10,),
        "card_hps": (10,),
        "card_has_attack": (10,),
        "card_has_defend": (10,),
        "card_mask": (10,)
    },


    # ================= Card Used =================

    "card_used": {

        "description": str,  # 卡牌描述文本
        # example: "When enters battlefield..."

        "special_type": (20,),  # 特殊能力 multi-hot

        "mana_cost": (6,),
        # [colorless, green, blue, red, white, black]
        # example: [2,1,0,0,0,0]

        "attack": int,     # example: 2
        "defend": int,     # example: 3
        "has_state": int,  # 是否存在该卡 (0/1)
        "card_type": int   # 使用 card_type enum
    }
}
"""
def get_state(room:"Base_Agent_Room",agent:"Agent"):
    state_batch={}

    oppo_agent=agent.opponent

    self_life=max(0,min(20,int(agent.life)))
    self_life_one_hot=np.zeros(21)
    self_life_one_hot[self_life]=1
    state_batch["self_life"]=self_life_one_hot

    oppo_life=max(0,min(20,int(oppo_agent.life)))
    oppo_life_one_hot=np.zeros(21)
    oppo_life_one_hot[oppo_life]=1
    state_batch["oppo_life"]=oppo_life_one_hot
    max_mana=20

    

    self_mana=[]
    cost=room.get_cost_total(agent)
    for color in ["U","R","G","W","B"]:
        mana_cost=cost[color]
        mana_cost=max(0,min(max_mana,int(mana_cost)))
        # one_hot=np.zeros(max_mana)
        # one_hot[mana_cost]=1
        self_mana.append(mana_cost)
    

    state_batch["self_mana"]=self_mana
        
    state_batch["action_history"]=agent.get_action_history()

    state_batch["card_hand"]=get_cards_state(room,agent,agent.hand,10)

    state_batch["card_library"]=get_cards_state(room,agent,agent.library,40)

    state_batch["card_graveyard"]=get_cards_state(room,agent,agent.graveyard,40)

    state_batch["self_board"]=get_creature_state_batch(room,agent,agent.battlefield)
    state_batch["oppo_board"]=get_creature_state_batch(room,agent,oppo_agent.battlefield)

    state_batch["stack"]=get_stack_state(room,agent,10)
    return state_batch


def get_stack_state(room:"Base_Agent_Room",agent:"Agent",max_length:int=10):
    stack=room.stack
    action2num=room.basic_func[agent.name]["action2num"]

    stack_cards=get_cards_state(room,agent,[stack_item["card"] for stack_item in stack],max_length)
    stack_actions=[]
    stack_players=[]
    for stack_item in stack:
        card=stack_item["card"]
        message=stack_item.get("message")
        if message:
            try:
                stack_actions.append(action2num(agent,message))
            except (ValueError,KeyError,IndexError,TypeError):
                stack_actions.append(0)
        else:
            stack_actions.append(0)
        stack_players.append([1,0] if card.player==agent else [0,1])

    while len(stack_actions)<max_length:
        stack_actions.append(0)
    while len(stack_players)<max_length:
        stack_players.append([0,0])

    return {
        "stack_cards":stack_cards,
        "player_one_hot":np.array(stack_players),
        "action_number":np.array(stack_actions[:max_length]),
    }

def get_cards_state(room:"Base_Agent_Room",agent:"Agent",cards:list["Card"],max_length:int=10):
    card_types=[]
    card_special_types=[]
    card_costs=[]
    card_atks=[]
    card_hps=[]
    card_has_attack=[]
    card_has_defend=[]
    card_mask=[]
    max_mana=20
    length_hand=len(cards)
    for hand_i in range(max_length):
        if hand_i <length_hand:
            card=cards[hand_i]

            

            card_type,card_special_type=room.get_card_special_types(card)

            card_types.append(card_type)
            card_special_types.append(card_special_type)

            card_manas=[]
            for mana in list(card.calculate_cost().values()):
                mana=max(0,min(max_mana,int(mana)))
                # mana_one_hot=np.zeros(max_mana)
                # mana_one_hot[mana]=1
                card_manas.append(mana)
            #card_manas=np.concatenate(card_manas, axis=0)
            #print(card.calculate_cost().values())
            card_costs.append(np.array(card_manas))

            if card_type==1:
                attack,defend=card.state
                card_atks.append(attack)
                card_hps.append(defend)
                card_has_attack.append(1)
                card_has_defend.append(1)
            else:
                card_atks.append(0)
                card_hps.append(0)
                card_has_attack.append(0)
                card_has_defend.append(0)

            card_mask.append(1)
        else:
            
            card_types.append(0)
            card_special_types.append(np.zeros(20))
            card_costs.append(np.zeros(6))
            card_atks.append(0)
            card_hps.append(0)
            card_has_attack.append(0)
            card_has_defend.append(0)
            card_mask.append(0)
    return {
        "card_types":np.array(card_types),
        "card_special_types":np.array(card_special_types),
        "card_costs":np.array(card_costs),
        "card_atks":np.array(card_atks),
        "card_hps":np.array(card_hps),
        "card_has_attack":np.array(card_has_attack),
        "card_has_defend":np.array(card_has_defend),
        "card_mask":np.array(card_mask)
    }

def get_creature_state(room:"Base_Agent_Room",creature:"Creature"):
    
    result={}
    _,card_special_type=room.get_card_special_types(creature)
    attack,defend=list(creature.state)

    result["card_special_types"]=[card_special_type]
    result["card_atks"]=[attack]
    result["card_hps"]=[defend]
    result["card_has_attack"]=[1]
    result["card_has_defend"]=[1]
    return result

def get_creature_state_batch(room:"Base_Agent_Room",agent:"Agent",creatures:list["Creature"]):
    length=len(creatures)
    batch_result={}
    batch_result["card_special_types"]=[]
    batch_result["card_atks"]=[]
    batch_result["card_hps"]=[]
    batch_result["card_has_attack"]=[]
    batch_result["card_has_defend"]=[]
    batch_result["card_mask"]=[]


    sort_function=room.create_sort_function(agent)
    cards_sorted = sorted(creatures, key=sort_function, reverse=True)
    #print(cards_sorted)
    for i in range(10):
        if i < length:
            creature=cards_sorted[i]
            result=get_creature_state(room,creature)
            batch_result["card_special_types"]+=result["card_special_types"]
            batch_result["card_atks"]+=result["card_atks"]
            batch_result["card_hps"]+=result["card_hps"]
            batch_result["card_has_attack"]+=result["card_has_attack"]
            batch_result["card_has_defend"]+=result["card_has_defend"]
            batch_result["card_mask"]+=[1]
        else:
            batch_result["card_special_types"]+=[np.zeros(20)]
            batch_result["card_atks"]+=[0]
            batch_result["card_hps"]+=[0]
            batch_result["card_has_attack"]+=[0]
            batch_result["card_has_defend"]+=[0]
            batch_result["card_mask"]+=[0]
    return batch_result