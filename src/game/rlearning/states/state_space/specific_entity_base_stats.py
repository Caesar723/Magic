"""Entity state variant that also exposes each creature's printed stats."""

import numpy as np

from game.rlearning.states.state_space import specific_entity as base


def _add_base_stats(zone, cards):
    """Attach each creature's base attack and maximum health to one zone."""
    base_atks = np.zeros_like(zone["card_atks"], dtype=np.float32)
    base_hps = np.zeros_like(zone["card_hps"], dtype=np.float32)
    for slot, card in enumerate(cards[:len(base_atks)]):
        if zone["card_has_state"][slot]:
            base_atks[slot] = base._normalized_value(card.power)
            base_hps[slot] = base._normalized_value(card.live)
    zone["card_base_atks"] = base_atks
    zone["card_base_hps"] = base_hps


def get_state(room, agent):
    """Build the entity state with both current and base creature stats."""
    state = base.get_state(room, agent)
    opponent = agent.opponent
    card_zones = {
        "hand": agent.hand,
        "library": agent.library,
        "graveyard": agent.graveyard,
        "stack_cards": [item["card"] for item in room.stack],
    }
    board_zones = {
        "self_board": agent.battlefield,
        "oppo_board": opponent.battlefield,
        "self_land": agent.land_area,
        "oppo_land": opponent.land_area,
    }
    for name, cards in card_zones.items():
        _add_base_stats(state["card_zones"][name], cards)
    for name, cards in board_zones.items():
        _add_base_stats(state["board_zones"][name], cards)
    return state
