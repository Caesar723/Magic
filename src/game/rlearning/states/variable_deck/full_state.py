from typing import TYPE_CHECKING
import numpy as np

from game.type_cards.creature import Creature
from game.action_validator import (
    get_card_select_range,
    validate_activate_ability,
    validate_end_bullet,
    validate_end_step,
    validate_play_card,
    validate_select_attacker,
    validate_select_defender
)

from game.rlearning.actions.state_space.index_base import num2subaction
from game.rlearning.states.state_space.specific_entity import color_identity
from game.rlearning.states.state_space import specific_entity


if TYPE_CHECKING:
    from game.agent import Agent_Player as Agent
    from game.base_agent_room import Base_Agent_Room
    from game.card import Card


def select_stage(room:"Base_Agent_Room",agent:"Agent",start_index,hand_card,select_range):
    candidate_actions=[]
    for sub_action in range(1,23):
        try:
            select_content=num2subaction(room,agent,sub_action,select_range)
        except IndexError:
            continue
        valid,_=validate_play_card(room,agent,hand_card,select_content)
        if valid:
            candidate_actions.append(get_candidate_action(room,hand_card,start_index+sub_action))
    return candidate_actions

def mask_hand(room:"Base_Agent_Room",agent:"Agent"):
    candidate_actions=[]
    start_index=32
    select_ranges={
        "all_roles","opponent_roles","your_roles","all_creatures","opponent_creatures",
        "your_creatures","all_lands","opponent_lands","your_lands"
    }
    for hand_card in agent.hand[:10]:
        select_range=get_card_select_range(hand_card) or getattr(hand_card,"select_range","")
        valid,_=validate_play_card(room,agent,hand_card,"")
        if valid:
            if select_range in select_ranges:
                candidate_actions+=select_stage(room,agent,start_index,hand_card,select_range)
            elif not select_range:
                candidate_actions.append(get_candidate_action(room,hand_card,start_index))
        start_index+=33
    return candidate_actions

def mask_land_abilities(room:"Base_Agent_Room",agent:"Agent"):
    """Expose usable land abilities in every priority window."""
    candidate_actions=[]
    for index,land in enumerate(agent.land_area[:10]):
        valid,_=validate_activate_ability(room,agent,land,"land_area")
        if valid:
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
    candidate_actions=[]
    valid,_=validate_end_step(room,agent)
    if valid:
        candidate_actions.append({"card_info":None,"index":0,"action":None})
    valid,_=validate_end_bullet(room,agent)
    if valid:
        candidate_actions.append({"card_info":None,"index":1,"action":None})
    for index,creat in enumerate(agent.battlefield[:10]):
        valid,_=validate_select_attacker(room,agent,creat)
        if valid:
            candidate_actions.append(get_candidate_action(room,creat,2+index))
    for index,creat in enumerate(agent.battlefield[:10]):
        valid,_=validate_select_defender(room,agent,creat)
        if valid:
            candidate_actions.append(get_candidate_action(room,creat,12+index))
    candidate_actions+=mask_land_abilities(room,agent)
    candidate_actions+=mask_hand(room,agent)
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
    state["candidate_actions"]=get_candidate_actions(room,agent)
    return state
