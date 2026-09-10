"""Entity-transition dataset that merges matching outside/birth cards."""

from __future__ import annotations

from copy import deepcopy

import numpy as np

from game.rlearning.datasets.state_space.EntityTransition import (
    EntityTransitionDataset,
    get_state,
)
from game.rlearning.states.state_space.specific_entity import (
    BOARD_ZONE_NAMES,
    CARD_ZONE_NAMES,
)


def _text(value):
    return " ".join(str(value or "").split()).casefold()


def _value(zone, field, index, default=""):
    values = zone.get(field)
    return default if values is None else values[index]


def _tuple(value):
    return tuple(np.asarray(value).reshape(-1).round(6).tolist())


def _key(zone, index):
    return (
        _text(_value(zone, "card_names", index)),
        _text(_value(zone, "card_descriptions", index)),
        _text(_value(zone, "card_mana_costs", index)),
        _tuple(_value(zone, "card_costs", index, [])),
        _text(_value(zone, "card_colors", index)),
        int(_value(zone, "card_types", index, 0)),
        _tuple(_value(zone, "card_color_identity", index, [])),
    )


def _entities(state):
    for collection, zone_names in (
        ("card_zones", CARD_ZONE_NAMES),
        ("board_zones", BOARD_ZONE_NAMES),
    ):
        for zone_name in zone_names:
            zone = state.get(collection, {}).get(zone_name)
            if not zone or "card_mask" not in zone:
                continue
            for index, (mask, card_id) in enumerate(
                zip(zone["card_mask"], zone["card_ids"])
            ):
                if float(mask) > 0.5:
                    yield {
                        "collection": collection,
                        "zone": zone_name,
                        "index": index,
                        "id": int(card_id),
                        "key": _key(zone, index),
                    }


def _valid(card):
    name, description, raw_cost, cost_values, _, _, identity = card["key"]
    return bool(name and description and raw_cost and cost_values and identity)


def merge_outside_birth_cards(source, target):
    """Copy ``target`` and link exact outside/birth matches by card ID."""
    source_cards = list(_entities(source))
    target_cards = list(_entities(target))
    source_ids = {card["id"] for card in source_cards}
    target_ids = {card["id"] for card in target_cards}

    outside = [
        card for card in source_cards
        if card["id"] not in target_ids and _valid(card)
    ]
    births = [
        card for card in target_cards
        if card["id"] not in source_ids and _valid(card)
    ]
    by_key = {}
    for card in births:
        by_key.setdefault(card["key"], []).append(card)

    result = deepcopy(target)
    merged = []
    for outside_card in outside:
        candidates = by_key.get(outside_card["key"], [])
        if not candidates:
            continue
        birth = candidates.pop(0)
        zone = result[birth["collection"]][birth["zone"]]
        zone["card_ids"][birth["index"]] = np.asarray(
            outside_card["id"], dtype=zone["card_ids"].dtype
        )
        merged.append({
            "name": outside_card["key"][0],
            "source_zone": outside_card["zone"],
            "source_card_id": outside_card["id"],
            "target_zone": birth["zone"],
            "birth_card_id": birth["id"],
        })
    return result, merged


class EntityTransitionMergedDataset(EntityTransitionDataset):
    """Dataset variant used only by the merged comparison experiment."""

    def get_sample(self, data):
        source = data["state"]
        target, _ = merge_outside_birth_cards(source, data["next_state"])
        result = {"state": get_state(source), "next_state": get_state(target)}

        action = int(data["action"])
        result["action"] = np.eye(
            self.config.get("action_space", 362), dtype=np.float32
        )[action]
        result["action_index"] = np.asarray(action, dtype=np.int64)

        card_used = dict(source["card_used"])
        card_used["description"] = self.augment_description(
            card_used["description"]
        )
        result["card_used"] = card_used
        return result
