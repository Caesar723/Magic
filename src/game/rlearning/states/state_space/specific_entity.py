from typing import TYPE_CHECKING

import numpy as np


if TYPE_CHECKING:
    from game.agent import Agent_Player as Agent
    from game.base_agent_room import Base_Agent_Room
    from game.card import Card


# ============================================================
# Entity schema
# ============================================================

CARD_ZONE_NAMES = (
    "hand",
    "library",
    "graveyard",
    "stack_cards",
)

BOARD_ZONE_NAMES = (
    "self_board",
    "oppo_board",
    "self_land",
    "oppo_land",
)

ENTITY_ZONE_NAMES = CARD_ZONE_NAMES + BOARD_ZONE_NAMES
LOCATION_NAMES = ENTITY_ZONE_NAMES + ("outside",)


# ============================================================
# Public state
# ============================================================

def get_state(room: "Base_Agent_Room", agent: "Agent"):
    """Build the entity-aligned state used by the location ablation."""
    opponent = agent.opponent
    attacker = getattr(room, "attacker", None)

    state = {
        "self_life": _normalized_value(agent.life),
        "oppo_life": _normalized_value(opponent.life),
        "self_mana": _get_mana_state(room, agent),
        "action_history": agent.get_action_history(),
        "card_zones": {
            "hand": get_card_entities(room, agent.hand, 10),
            "library": get_card_entities(room, agent.library, 40),
            "graveyard": get_card_entities(room, agent.graveyard, 40),
        },
        "board_zones": {
            "self_board": get_card_entities(
                room,
                agent.battlefield,
                10,
                dynamic_state=True,
                attacker=attacker,
            ),
            "oppo_board": get_card_entities(
                room,
                opponent.battlefield,
                10,
                dynamic_state=True,
                attacker=attacker,
            ),
            "self_land": get_card_entities(
                room,
                agent.land_area,
                20,
                dynamic_state=True,
            ),
            "oppo_land": get_card_entities(
                room,
                opponent.land_area,
                20,
                dynamic_state=True,
            ),
        },
    }

    stack_cards, stack_extra = get_stack_entities(room, agent, max_length=10)
    state["card_zones"]["stack_cards"] = stack_cards
    state["stack_extra"] = stack_extra
    return state


# ============================================================
# Global values
# ============================================================

def _normalized_value(value, maximum=20):
    value = max(0, min(maximum, int(value)))
    return value / maximum


def _get_mana_state(room: "Base_Agent_Room", agent: "Agent"):
    """Keep the existing global mana semantics unchanged."""
    total_cost = room.get_cost_total(agent)
    return np.asarray(
        [
            _normalized_value(total_cost[color])
            for color in ("U", "R", "G", "W", "B")
        ],
        dtype=np.float32,
    )


# ============================================================
# Card entities
# ============================================================

def _empty_entity():
    return {
        "card_ids": -1,
        "card_types": 0,
        "card_special_types": np.zeros(20, dtype=np.float32),
        "card_costs": np.zeros(6, dtype=np.float32),
        "card_atks": 0.0,
        "card_hps": 0.0,
        "card_has_state": 0.0,
        "card_tapped": 0.0,
        "card_tapped_valid": 0.0,
        "card_is_attacker": 0.0,
        "card_mask": 0.0,
    }


def _card_entity(room: "Base_Agent_Room", card: "Card", dynamic_state: bool, is_attacker: bool = False):
    """Encode one card and retain its current combat-attacker role."""
    card_type, special_types = room.get_card_special_types(card)
    costs = [
        max(0, min(20, int(value)))
        for value in card.calculate_cost().values()
    ]

    has_state = float(card_type == 1)
    attack = 0.0
    health = 0.0
    if has_state:
        attack, health = card.state
        attack = _normalized_value(attack)
        health = _normalized_value(health)

    return {
        "card_ids": np.int64(card.card_id),
        "card_types": np.int64(card_type),
        "card_special_types": np.asarray(special_types, dtype=np.float32),
        "card_costs": np.asarray(costs, dtype=np.float32),
        "card_atks": np.float32(attack),
        "card_hps": np.float32(health),
        "card_has_state": np.float32(has_state),
        "card_tapped": np.float32(card.get_flag("tap")) if dynamic_state else np.float32(0.0),
        "card_tapped_valid": np.float32(dynamic_state),
        "card_is_attacker": np.float32(is_attacker),
        "card_mask": np.float32(1.0),
    }


def get_card_entities(
    room: "Base_Agent_Room",
    cards: list["Card"],
    max_length: int,
    *,
    dynamic_state: bool = False,
    attacker: "Card | None" = None,
):
    """Encode one zone and mark the slot that contains the live attacker."""
    fields = {name: [] for name in _empty_entity()}

    for slot_index in range(max_length):
        if slot_index < len(cards):
            card = cards[slot_index]
            entity = _card_entity(room, card, dynamic_state, card is attacker)
        else:
            entity = _empty_entity()

        for name, value in entity.items():
            fields[name].append(value)

    return {
        name: np.asarray(values)
        for name, values in fields.items()
    }


# ============================================================
# Stack
# ============================================================

def get_stack_entities(
    room: "Base_Agent_Room",
    agent: "Agent",
    *,
    max_length: int,
):
    stack = room.stack
    action_to_number = room.basic_func[agent.name]["action2num"]

    cards = [item["card"] for item in stack]
    card_entities = get_card_entities(room, cards, max_length)

    actions = []
    players = []
    for item in stack[:max_length]:
        card = item["card"]
        message = item.get("message")

        if message:
            try:
                actions.append(action_to_number(agent, message))
            except (ValueError, KeyError, IndexError, TypeError):
                actions.append(0)
        else:
            actions.append(0)

        players.append([1, 0] if card.player == agent else [0, 1])

    while len(actions) < max_length:
        actions.append(0)
        players.append([0, 0])

    stack_extra = {
        "player_one_hot": np.asarray(players, dtype=np.float32),
        "action_number": np.asarray(actions, dtype=np.int64),
    }
    return card_entities, stack_extra
