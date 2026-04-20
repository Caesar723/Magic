
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.base_agent_room import Base_Agent_Room
    from game.agent import Agent_Player as Agent
    from game.type_cards.creature import Creature
    from game.type_cards.instant import Instant
    from game.type_cards.land import Land
    from game.type_cards.sorcery import Sorcery
    from game.card import Card


"""
Our hero's health, length 20:
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0] # Health is 19

Opponent's hero health, length 20:
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0] # Health is 19

Mana:
Green, length 20: [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # 0
Blue, length 20:  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1] # 20
Red, length 20:   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
White, length 20: [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Black, length 20: [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

Hand, length 10:
    For each card:
    Card ID for nn.embedding
    Card type (4 types) for nn.embedding
    Special types, length 20:
    [battlecry, deathrattle, reach, trample, flying, haste, flash, lifelink, summoning_sickness, padding]

    Combined, total length 120
    Colorless mana, length 20: [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    Green mana, length 20:     [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    Blue mana, length 20:      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    Red mana, length 20:       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    White mana, length 20:     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    Black mana, length 20:     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    Attack and defense:
    [atk_n, hp_n]
    [has_attack, has_defend]

Battlefield, length 10:
    For each creature:
    Special types, length 20:
    [battlecry, deathrattle, reach, trample, flying, haste, flash, lifelink, summoning_sickness, padding]
    [atk_n, hp_n]
    [has_attack, has_defend]

Opponent battlefield, length 10:
    For each creature:
    Special types, length 20:
    [battlecry, deathrattle, reach, trample, flying, haste, flash, lifelink, summoning_sickness, padding]
    [atk_n, hp_n]
    [has_attack, has_defend]

Attacking creature embedding:
Attack and defense:
[atk_n, hp_n]
[has_attack, has_defend]
[battlecry, deathrattle, reach, trample, flying, haste, flash, lifelink, summoning_sickness, padding]
"""
def get_state(room:"Base_Agent_Room",agent:"Agent"):
    state_batch={}

    basic_state=[]
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

    card_ids=[]
    card_types=[]
    card_special_types=[]
    card_costs=[]
    card_atks=[]
    card_hps=[]
    card_has_attack=[]
    card_has_defend=[]
    card_mask=[]
    
    length_hand=len(agent.hand)
    for hand_i in range(10):
        if hand_i <length_hand:
            card=agent.hand[hand_i]

            card_ids.append(agent.id_dict[f"{card.name}+{card.type}"])

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
            card_ids.append(0)
            card_types.append(0)
            card_special_types.append(np.zeros(20))
            card_costs.append(np.zeros(6))
            card_atks.append(0)
            card_hps.append(0)
            card_has_attack.append(0)
            card_has_defend.append(0)
            card_mask.append(0)


    state_batch["card_hand"]={}
    state_batch["card_hand"]["card_ids"]=np.array(card_ids)
    state_batch["card_hand"]["card_types"]=np.array(card_types)
    state_batch["card_hand"]["card_special_types"]=np.array(card_special_types)
    state_batch["card_hand"]["card_costs"]=np.array(card_costs)
    state_batch["card_hand"]["card_atks"]=np.array(card_atks)
    state_batch["card_hand"]["card_hps"]=np.array(card_hps)
    state_batch["card_hand"]["card_has_attack"]=np.array(card_has_attack)
    state_batch["card_hand"]["card_has_defend"]=np.array(card_has_defend)
    state_batch["card_hand"]["card_mask"]=np.array(card_mask)

    state_batch["self_board"]=get_creature_state_batch(room,agent,agent.battlefield)
    state_batch["oppo_board"]=get_creature_state_batch(room,agent,oppo_agent.battlefield)

    
    if room.get_flag("attacker_defenders"):
        state_batch["attacker"]=get_creature_state(room,room.attacker)
        
    else:
        state_batch["attacker"]={}
        state_batch["attacker"]["card_special_types"]=[np.zeros(20)]
        state_batch["attacker"]["card_atks"]=[0]
        state_batch["attacker"]["card_hps"]=[0]
        state_batch["attacker"]["card_has_attack"]=[0]
        state_batch["attacker"]["card_has_defend"]=[0]

    return state_batch



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