import numpy as np

from game.rlearning.datasets.state_space.CVAE import (
    CVAEDataset,
    ensure_list,
    stack_path_numpy,
)
from game.rlearning.states.state_space.specific_entity import (
    BOARD_ZONE_NAMES,
    CARD_ZONE_NAMES,
)


# ============================================================
# Raw state -> structured entity state
# ============================================================

def collate_entity_zone_numpy(batch, collection: str, zone_name: str):
    prefix = f"{collection}&{zone_name}"
    return {
        "card_ids": stack_path_numpy(
            batch,
            f"{prefix}&card_ids",
            dtype=np.int64,
        ),
        "card_types": stack_path_numpy(
            batch,
            f"{prefix}&card_types",
            dtype=np.int64,
        ),
        "card_costs": stack_path_numpy(
            batch,
            f"{prefix}&card_costs",
            dtype=np.float32,
        ),
        "card_special_types": stack_path_numpy(
            batch,
            f"{prefix}&card_special_types",
            dtype=np.float32,
        ),
        "card_atks": stack_path_numpy(
            batch,
            f"{prefix}&card_atks",
            dtype=np.float32,
        ),
        "card_hps": stack_path_numpy(
            batch,
            f"{prefix}&card_hps",
            dtype=np.float32,
        ),
        "card_has_state": stack_path_numpy(
            batch,
            f"{prefix}&card_has_state",
            dtype=np.float32,
        ),
        "card_tapped": stack_path_numpy(
            batch,
            f"{prefix}&card_tapped",
            dtype=np.float32,
        ),
        "card_tapped_valid": stack_path_numpy(
            batch,
            f"{prefix}&card_tapped_valid",
            dtype=np.float32,
        ),
        "card_mask": stack_path_numpy(
            batch,
            f"{prefix}&card_mask",
            dtype=np.float32,
        ),
    }


def get_state(data):
    """Convert raw entity states into the model's nested tensor schema."""
    data = ensure_list(data)
    num_frames = len(data)

    self_life = stack_path_numpy(
        data,
        "self_life",
        dtype=np.float32,
    ).reshape(num_frames, -1)
    oppo_life = stack_path_numpy(
        data,
        "oppo_life",
        dtype=np.float32,
    ).reshape(num_frames, -1)
    self_mana = stack_path_numpy(
        data,
        "self_mana",
        dtype=np.float32,
    ).reshape(num_frames, -1)

    global_state = np.concatenate(
        [self_life, oppo_life, self_mana],
        axis=-1,
    ).astype(np.float32)

    card_zones = {
        zone_name: collate_entity_zone_numpy(
            data,
            "card_zones",
            zone_name,
        )
        for zone_name in CARD_ZONE_NAMES
    }
    board_zones = {
        zone_name: collate_entity_zone_numpy(
            data,
            "board_zones",
            zone_name,
        )
        for zone_name in BOARD_ZONE_NAMES
    }
    stack_extra = {
        "player_one_hot": stack_path_numpy(
            data,
            "stack_extra&player_one_hot",
            dtype=np.float32,
        ),
        "action_number": stack_path_numpy(
            data,
            "stack_extra&action_number",
            dtype=np.int64,
        ),
    }

    return {
        "global_state": global_state,
        "card_zones": card_zones,
        "board_zones": board_zones,
        "stack_extra": stack_extra,
    }


# ============================================================
# Dataset
# ============================================================

class EntityTransitionDataset(CVAEDataset):
    """CVAE dataset with card-instance metadata for transition alignment."""

    def get_sample(self, data):
        result = {
            "state": get_state(data["state"]),
            "next_state": get_state(data["next_state"]),
        }

        action = int(data["action"])
        action_one_hot = np.zeros(
            self.config.get("action_space", 362),
            dtype=np.float32,
        )
        action_one_hot[action] = 1.0

        result["action"] = action_one_hot
        result["action_index"] = np.asarray(action, dtype=np.int64)
        card_used = dict(data["state"]["card_used"])
        description = card_used["description"]
        card_used["description"] = self.augment_description(description)
        result["card_used"] = card_used
        return result
