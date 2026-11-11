from copy import deepcopy

import numpy as np
import torch

from game.rlearning.datasets.state_space.EntityTransitionMerged import (
    EntityTransitionMergedDataset,
)
from game.rlearning.states.state_space.specific_entity import (
    BOARD_ZONE_NAMES,
    CARD_ZONE_NAMES,
)


def flatten_entity_ids(state):
    ids, masks = [], []

    for collection, zone_names in (
        ("card_zones", CARD_ZONE_NAMES),
        ("board_zones", BOARD_ZONE_NAMES),
    ):
        for zone_name in zone_names:
            zone = state[collection][zone_name]
            ids.append(np.asarray(zone["card_ids"]).reshape(-1))
            masks.append(np.asarray(zone["card_mask"]).reshape(-1) > 0.5)

    return np.concatenate(ids), np.concatenate(masks)


class ConditionEventDataset(EntityTransitionMergedDataset):
    def set_extra(self):
        self.extra = {}

    def augment_description(self, description):
        return description

    def get_sample(self, data):
        result = super().get_sample(data)
        source = data["state"]
        targets = source.get("event_targets") or {}
        entity_ids, entity_mask = flatten_entity_ids(source)
        dead_ids = {int(card_id) for card_id in targets.get("dead_ids", [])}

        result["entity_died"] = np.asarray(
            [float(card_id in dead_ids) for card_id in entity_ids],
            dtype=np.float32,
        )
        result["entity_mask"] = entity_mask.astype(np.bool_)
        result["player_damage"] = np.asarray(
            targets.get("player_damage", [0, 0]), dtype=np.int64
        )
        result["player_heal"] = np.asarray(
            targets.get("player_heal", [0, 0]), dtype=np.int64
        )
        result["draw_counts"] = np.asarray(
            targets.get("draw_counts", [0, 0]), dtype=np.int64
        )
        result["event_valid"] = np.asarray(
            targets.get("version") == 1, dtype=np.bool_
        )

        supervision = deepcopy(source["card_used"].get("supervision") or {})
        supervision.setdefault("source_id", None)
        supervision.setdefault("text_parts", [])
        supervision.setdefault("spans", {})
        supervision.setdefault("fields", [])
        result["supervision"] = supervision
        return result

    def collate_fn(self, batch):
        result = super().collate_fn(batch)
        fields = (
            "entity_died",
            "entity_mask",
            "player_damage",
            "player_heal",
            "draw_counts",
            "event_valid",
        )

        for name in fields:
            result[name] = torch.from_numpy(
                np.stack([sample[name] for sample in batch])
            )

        result["supervision"] = [
            sample["supervision"] for sample in batch
        ]
        return result