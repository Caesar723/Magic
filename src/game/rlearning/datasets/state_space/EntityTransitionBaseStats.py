"""Dataset collation for the entity state with base creature stats."""

import numpy as np

from game.rlearning.datasets.state_space.CVAE import ensure_list, stack_path_numpy
from game.rlearning.datasets.state_space.EntityTransition import EntityTransitionDataset
from game.rlearning.states.state_space.specific_entity import BOARD_ZONE_NAMES, CARD_ZONE_NAMES


def _add_base_stats(state, raw_states):
    """Stack the two base-stat channels into an already collated entity state."""
    raw_states = ensure_list(raw_states)
    for collection, names in (("card_zones", CARD_ZONE_NAMES), ("board_zones", BOARD_ZONE_NAMES)):
        for name in names:
            prefix = f"{collection}&{name}"
            zone = state[collection][name]
            zone["card_base_atks"] = stack_path_numpy(raw_states, f"{prefix}&card_base_atks", np.float32)
            zone["card_base_hps"] = stack_path_numpy(raw_states, f"{prefix}&card_base_hps", np.float32)
    return state


class EntityTransitionBaseStatsDataset(EntityTransitionDataset):
    """Collate transitions collected with the base-stat entity state."""

    def get_sample(self, data):
        """Keep the standard transition sample and add the two new channels."""
        sample = super().get_sample(data)
        sample["state"] = _add_base_stats(sample["state"], data["state"])
        sample["next_state"] = _add_base_stats(sample["next_state"], data["next_state"])
        return sample
