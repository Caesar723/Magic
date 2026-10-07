from typing import TYPE_CHECKING
import numpy as np

from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.rlearning.states.state_space.specific_entity import color_identity
from game.rlearning.states.state_space import specific_entity


if TYPE_CHECKING:
    from game.agent import Agent_Player as Agent
    from game.base_agent_room import Base_Agent_Room
    from game.card import Card


def select_stage(room:"Base_Agent_Room",selects,index_range,start_index,hand_card):
    index=start_index
    candidate_actions=[]
    for select_list,ind_range in zip(selects,index_range):
        length=min(len(select_list),10)
        for i in range(length):
            candidate_actions.append(get_candidate_action(room,hand_card,index+i))
        index+=ind_range
    return candidate_actions

def get_card_select_range(card):
    instance_dict={
        Creature:"when_enter_battlefield",
        Instant:"card_ability",
        Land:"when_enter_landarea",
        Sorcery:"card_ability"
    }
    for cls, ability_name in instance_dict.items():
        if isinstance(card,cls):
            return getattr(card,ability_name).select_range
    return ""

def mask_hand(room:"Base_Agent_Room",agent:"Agent",oppo_agent:"Agent"):
    candidate_actions=[]
    start_index=32

    select_dict={
        'all_roles':[oppo_agent.battlefield,agent.battlefield,[1],[1]],
        'opponent_roles':[oppo_agent.battlefield,[],[],[1]], 
        'your_roles':[[],agent.battlefield,[1],[]],
        'all_creatures':[oppo_agent.battlefield,agent.battlefield,[],[]],
        'opponent_creatures':[oppo_agent.battlefield,[],[],[]],
        'your_creatures':[[],agent.battlefield,[],[]],
        'all_lands':[oppo_agent.land_area,agent.land_area,[],[]],
        'opponent_lands':[oppo_agent.land_area,[],[],[]],
        'your_lands':[[],agent.land_area,[],[]]
    }

    index_range=[10,10,1,1]
    #getattr(obj, 'my_attribute')
    card_counter=0
    for hand_card in agent.hand:
        if card_counter>=10:
            break

        if room.get_flag("bullet_time"):
            if not isinstance(hand_card,Instant) and not hand_card.get_flag("Flash"):
                start_index+=33
                card_counter+=1
                continue
        
        if hand_card.check_can_use(agent)[0]:
            select_range=get_card_select_range(hand_card)
            #print(select_range)
            if select_range in select_dict:
                candidate_actions+=select_stage(select_dict[select_range],index_range,start_index+1,hand_card)#+1 是因为有player a card 不选择
            elif hand_card.select_range in select_dict:
                candidate_actions+=select_stage(select_dict[hand_card.select_range],index_range,start_index+1,hand_card)
            else:

                candidate_actions.append(get_candidate_action(room,hand_card,start_index))
        start_index+=33
        card_counter+=1
    return candidate_actions


def mask_land_abilities(room:"Base_Agent_Room",agent:"Agent",oppo_agent:"Agent"):
    """Expose usable land abilities in every priority window."""
    candidate_actions=[]
    for index, land in enumerate(agent.land_area[:10]):
        if not land.get_flag("tap") and land.check_ability_can_be_used(agent, oppo_agent) and land.content!="":
            candidate_actions.append(get_candidate_action(room,land,22+index))
            
    return candidate_actions




def index_to_action(index: int):
    """Convert a 362-dimensional action index to an action value."""
    if not 0 <= index < 362:
        raise ValueError(f"index must be between 0 and 361, got {index}")
    if index in (0, 1):  # Special actions: pass or finish blocking
        return None
    if 2 <= index <= 11:  # Attack
        return 0
    if 12 <= index <= 21:  # Block
        return 1
    if 22 <= index <= 31:  # Activate a land ability
        return 2
    sub_action = (index - 32) % 33  # Play sub-action: 0-32
    return 3 + sub_action

def get_candidate_action(room: "Base_Agent_Room",card:"Card",index:int):
    card_type, special_type = room.get_card_special_types(card)
    max_value = 20
    mana_cost = np.asarray([
        max(0, min(max_value, int(value))) / max_value
        for value in card.calculate_cost().values()
    ], dtype=np.float32)
    if isinstance(card, Creature):
        attack, defend = card.state
        attack = max(0, min(max_value, int(attack))) / max_value
        defend = max(0, min(max_value, int(defend))) / max_value
        has_state = 1
    else:
        attack, defend, has_state = 0.0, 0.0, 0
    card_info = {
        "description": card.content,
        "special_type": np.asarray(special_type, dtype=np.float32),
        "mana_cost": mana_cost,
        "color_identity": color_identity(card.mana_cost, card.color, card.name),
        "attack": attack,
        "defend": defend,
        "has_state": has_state,
        "card_type": card_type,
    }
    return {
        "card_info": card_info,
        "index": index,
        "action":index_to_action(index)
    }

def get_candidate_actions(room:"Base_Agent_Room",agent:"Agent"):
    oppo_agent=agent.opponent
    candidate_actions=[]
    candidate_actions+=mask_land_abilities(room,agent,oppo_agent)
    if room.get_flag('attacker_defenders'):

        candidate_actions.append({"card_info":None,"index":1,"action":None})
        for i,creat in enumerate(agent.battlefield):
            if i>=10:break
            if not creat.get_flag("tap") and \
    (not room.attacker.get_flag("flying") or (creat.get_flag("flying") or creat.get_flag("reach"))):
                candidate_actions.append(get_candidate_action(room,creat,12+i))
        #if agent.battlefield: mask[12:len(agent.battlefield)+12]=True
        if agent.hand:
            candidate_actions+=mask_hand(room,agent,oppo_agent)
    elif room.get_flag("bullet_time"):
        candidate_actions.append({"card_info":None,"index":1,"action":None})
        if agent.hand:
            candidate_actions+=mask_hand(room,agent,oppo_agent)
    else:

        candidate_actions.append({"card_info":None,"index":0,"action":None})
        for i,creat in enumerate(agent.battlefield):
            if i>=10:break
            if (not creat.get_flag("summoning_sickness") or creat.get_flag("haste")) and\
    not creat.get_flag("tap") and (creat.get_counter_from_dict("attack_counter")>0):
                candidate_actions.append(get_candidate_action(room,creat,2+i))
        #if agent.battlefield: mask[2:len(agent.battlefield)+2]=True
        if agent.hand:
            candidate_actions+=mask_hand(room,agent,oppo_agent)
    #print(mask)
    return candidate_actions


def _card_info(cards, size):
    fields = {
        "card_names": "name",
        "card_descriptions": "content",
        "card_mana_costs": "mana_cost",
        "card_colors": "color",
    }
    result = {name: [""] * size for name in fields}
    for index, card in enumerate(cards[:size]):
        for field, attribute in fields.items():
            result[field][index] = str(getattr(card, attribute, ""))
    return {
        name: np.asarray(values, dtype=object)
        for name, values in result.items()
    }

def get_state_from_player(room, agent):
    state = specific_entity.get_state(room, agent)
    opponent = agent.opponent
    del state["action_history"]#action history is not used in the state space
    zones = {
        "card_zones": {
            "hand": (agent.hand, 10),
            "library": (agent.library, 40),
            "graveyard": (agent.graveyard, 40),
            "stack_cards": ([item["card"] for item in room.stack], 10),
        },
        "board_zones": {
            "self_board": (agent.battlefield, 10),
            "oppo_board": (opponent.battlefield, 10),
            "self_land": (agent.land_area, 20),
            "oppo_land": (opponent.land_area, 20),
        },
    }
    for collection, collection_zones in zones.items():
        for zone, (cards, size) in collection_zones.items():
            state[collection][zone].update(_card_info(cards, size))
    
    return state


def get_state(room, agent):
    state=get_state_from_player(room, agent)
    state["oppo_state"]=get_state_from_player(room, agent.opponent)
    state["candidate_actions"]=get_candidate_actions(room,agent)
    return state

