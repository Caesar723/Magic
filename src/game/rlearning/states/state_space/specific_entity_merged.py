"""Raw entity state with card identity fields for the merge experiment."""

from __future__ import annotations

import numpy as np

from game.rlearning.states.state_space import specific_entity


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


def get_state(room, agent):
    state = specific_entity.get_state(room, agent)
    opponent = agent.opponent
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
