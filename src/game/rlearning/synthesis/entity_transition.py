"""Convert source-aligned entity transitions into reconstruction artifacts."""

from __future__ import annotations

from typing import Any

import torch
import torch.nn.functional as F

from game.rlearning.states.state_space.specific_entity import (
    BOARD_ZONE_NAMES,
    CARD_ZONE_NAMES,
    LOCATION_NAMES,
)
from game.rlearning.synthesis.state_space import (
    CARD_TYPE_NAMES,
    MANA_NAMES,
    SPECIAL_TYPE_NAMES,
)


ENTITY_FIELDS = (
    "card_ids",
    "card_types",
    "card_costs",
    "card_special_types",
    "card_atks",
    "card_hps",
    "card_has_state",
    "card_tapped",
    "card_tapped_valid",
    "card_is_attacker",
    "card_mask",
)

PREDICTION_FIELDS = (
    "destination_zone",
    "card_special_types",
    "card_atks",
    "card_hps",
    "card_has_state",
    "card_tapped",
)


# ============================================================
# Entity alignment
# ============================================================

def iter_entity_zones(state):
    for zone_name in CARD_ZONE_NAMES:
        yield zone_name, state["card_zones"][zone_name]
    for zone_name in BOARD_ZONE_NAMES:
        yield zone_name, state["board_zones"][zone_name]


def flatten_state_entities(state):
    """Flatten all entity zones while retaining each source zone index."""
    flattened = {
        field_name: torch.cat(
            [zone[field_name] for _, zone in iter_entity_zones(state)],
            dim=1,
        )
        for field_name in ENTITY_FIELDS
    }

    batch_size = flattened["card_mask"].shape[0]
    device = flattened["card_mask"].device
    zone_indices = []
    for zone_index, (_, zone) in enumerate(iter_entity_zones(state)):
        zone_indices.append(
            torch.full(
                (batch_size, zone["card_mask"].shape[1]),
                zone_index,
                dtype=torch.long,
                device=device,
            )
        )
    flattened["zone_indices"] = torch.cat(zone_indices, dim=1)
    return flattened


def flatten_entity_predictions(prediction):
    return {
        field_name: torch.cat(
            [zone[field_name] for _, zone in iter_entity_zones(prediction)],
            dim=1,
        )
        for field_name in PREDICTION_FIELDS
    }


def _gather_slots(values, slot_indices):
    gather_indices = slot_indices
    while gather_indices.ndim < values.ndim:
        gather_indices = gather_indices.unsqueeze(-1)
    gather_indices = gather_indices.expand(
        *slot_indices.shape,
        *values.shape[2:],
    )
    return torch.gather(values, dim=1, index=gather_indices)


def align_next_entities(source, target):
    """Match next-state targets to source-card order using instance IDs."""
    source_entities = flatten_state_entities(source)
    target_entities = flatten_state_entities(target)

    source_valid = source_entities["card_mask"].bool()
    target_valid = target_entities["card_mask"].bool()
    id_matches = (
        source_entities["card_ids"].unsqueeze(-1)
        == target_entities["card_ids"].unsqueeze(1)
    ) & source_valid.unsqueeze(-1) & target_valid.unsqueeze(1)

    # Stack entries may temporarily duplicate a card in another engine list.
    # Keep same-zone copies first, then pair the remaining cross-zone movement.
    same_zone = (
        source_entities["zone_indices"].unsqueeze(-1)
        == target_entities["zone_indices"].unsqueeze(1)
    )
    same_zone_matches = id_matches & same_zone
    source_has_same_zone = same_zone_matches.any(dim=-1)
    target_used_in_same_zone = same_zone_matches.any(dim=1)
    cross_zone_matches = (
        id_matches
        & ~source_has_same_zone.unsqueeze(-1)
        & ~target_used_in_same_zone.unsqueeze(1)
    )
    preferred_matches = same_zone_matches | cross_zone_matches

    matched = preferred_matches.any(dim=-1)
    target_indices = preferred_matches.long().argmax(dim=-1)
    aligned_target = {
        field_name: _gather_slots(values, target_indices)
        for field_name, values in target_entities.items()
        if field_name != "zone_indices"
    }
    target_zone = _gather_slots(
        target_entities["zone_indices"],
        target_indices,
    )
    outside_index = LOCATION_NAMES.index("outside")
    aligned_target["destination_zone"] = torch.where(
        matched,
        target_zone,
        torch.full_like(target_zone, outside_index),
    )
    aligned_target["matched"] = matched
    return source_entities, aligned_target


# ============================================================
# Display-state conversion
# ============================================================

def _as_float(value: torch.Tensor) -> float:
    return float(value.detach().cpu().item())


def _as_int(value: torch.Tensor) -> int:
    return int(value.detach().cpu().item())


def _normalized_stat(value: torch.Tensor) -> int:
    return max(0, min(20, round(_as_float(value) * 20)))


def _mana_cost(values: torch.Tensor) -> list[int]:
    return [
        max(0, min(20, round(float(value))))
        for value in values.detach().cpu().flatten().tolist()
    ]


def _special_types(values: torch.Tensor, *, logits: bool) -> list[str]:
    values = values.detach().cpu()
    if logits:
        values = torch.sigmoid(values)
    indices = torch.nonzero(values >= 0.5, as_tuple=False).flatten().tolist()
    return [
        SPECIAL_TYPE_NAMES.get(index, f"Trait {index}")
        for index in indices
    ]


def _global_from_target(values: torch.Tensor) -> dict[str, Any]:
    values = values.detach().cpu().flatten()
    return {
        "self_life": _normalized_stat(values[0]),
        "oppo_life": _normalized_stat(values[1]),
        "mana": {
            name: _normalized_stat(values[2 + offset])
            for offset, name in enumerate(MANA_NAMES)
        },
    }


def _global_from_prediction(values: torch.Tensor) -> dict[str, Any]:
    classes = values.detach().cpu().argmax(dim=-1).tolist()
    return {
        "self_life": classes[0],
        "oppo_life": classes[1],
        "mana": {
            name: classes[2 + offset]
            for offset, name in enumerate(MANA_NAMES)
        },
    }


def _target_card(zone, slot_index):
    if _as_float(zone["card_mask"][slot_index]) <= 0.5:
        return None

    card = {
        "slot": slot_index + 1,
        "card_id": _as_int(zone["card_ids"][slot_index]),
        "type": CARD_TYPE_NAMES.get(
            _as_int(zone["card_types"][slot_index]),
            "Unknown",
        ),
        "mana_cost": _mana_cost(zone["card_costs"][slot_index]),
        "attack": _normalized_stat(zone["card_atks"][slot_index]),
        "health": _normalized_stat(zone["card_hps"][slot_index]),
        "has_state": _as_float(zone["card_has_state"][slot_index]) >= 0.5,
        "special_types": _special_types(
            zone["card_special_types"][slot_index],
            logits=False,
        ),
        "presence_confidence": 1.0,
    }
    if _as_float(zone["card_tapped_valid"][slot_index]) >= 0.5:
        card["tapped"] = _as_float(zone["card_tapped"][slot_index]) >= 0.5
    card["is_attacker"] = _as_float(zone["card_is_attacker"][slot_index]) >= 0.5
    return card


def _zone_from_target(zone):
    cards = [
        card
        for slot_index in range(zone["card_mask"].shape[0])
        if (card := _target_card(zone, slot_index)) is not None
    ]
    return {
        "card_count": len(cards),
        "slot_count": int(zone["card_mask"].shape[0]),
        "cards": cards,
    }


def _select_zone(zone, sample_index):
    return {
        field_name: values[sample_index]
        for field_name, values in zone.items()
    }


def _stack_context(state, sample_index):
    stack_extra = state.get("stack_extra")
    if not isinstance(stack_extra, dict):
        return {}

    players = stack_extra.get("player_one_hot")
    actions = stack_extra.get("action_number")
    if not isinstance(players, torch.Tensor) or not isinstance(actions, torch.Tensor):
        return {}

    players = players[sample_index].detach().cpu()
    actions = actions[sample_index].detach().cpu().flatten()
    context = {}
    for slot_index in range(min(players.shape[0], actions.shape[0])):
        player = players[slot_index]
        action = int(actions[slot_index].item())
        if float(player.max().item()) <= 0.5 and action == 0:
            continue
        if float(player.max().item()) <= 0.5:
            player_name = "Unknown"
        else:
            player_name = "Self" if int(player.argmax().item()) == 0 else "Opponent"
        context[slot_index] = {
            "stack_player": player_name,
            "stack_action": action,
        }
    return context


def state_from_entity_target(state, sample_index):
    """Create the UI state for a real source or next entity state."""
    display_state = {
        "global_state": _global_from_target(state["global_state"][sample_index]),
        "card_zones": {
            zone_name: _zone_from_target(
                _select_zone(state["card_zones"][zone_name], sample_index)
            )
            for zone_name in CARD_ZONE_NAMES
        },
        "board_zones": {
            zone_name: _zone_from_target(
                _select_zone(state["board_zones"][zone_name], sample_index)
            )
            for zone_name in BOARD_ZONE_NAMES
        },
    }

    stack_context = _stack_context(state, sample_index)
    for card in display_state["card_zones"]["stack_cards"]["cards"]:
        card.update(stack_context.get(card["slot"] - 1, {}))
    return display_state


def _empty_prediction_state(source):
    card_zones = {
        zone_name: {
            "card_count": 0,
            "slot_count": int(
                source["card_zones"][zone_name]["card_mask"].shape[1]
            ),
            "cards": [],
        }
        for zone_name in CARD_ZONE_NAMES
    }
    board_zones = {
        zone_name: {
            "card_count": 0,
            "slot_count": int(
                source["board_zones"][zone_name]["card_mask"].shape[1]
            ),
            "cards": [],
        }
        for zone_name in BOARD_ZONE_NAMES
    }
    return {
        "decode_label": "entity location-decoded",
        "global_state": {},
        "card_zones": card_zones,
        "board_zones": board_zones,
        "overflow_count": 0,
    }


def state_from_entity_prediction(prediction, source, sample_index):
    """Place each source card into the zone selected by location logits."""
    source_entities = flatten_state_entities(source)
    predicted_entities = flatten_entity_predictions(prediction)
    display_state = _empty_prediction_state(source)
    display_state["global_state"] = _global_from_prediction(
        prediction["global_state"][sample_index]
    )

    source_valid = source_entities["card_mask"][sample_index].bool()
    location_probs = F.softmax(
        predicted_entities["destination_zone"][sample_index],
        dim=-1,
    )
    predicted_zones = location_probs.argmax(dim=-1)

    for entity_index in torch.nonzero(source_valid, as_tuple=False).flatten().tolist():
        destination_index = int(predicted_zones[entity_index].item())
        destination_name = LOCATION_NAMES[destination_index]
        if destination_name == "outside":
            continue

        collection = (
            "card_zones"
            if destination_name in CARD_ZONE_NAMES
            else "board_zones"
        )
        zone = display_state[collection][destination_name]
        if len(zone["cards"]) >= zone["slot_count"]:
            display_state["overflow_count"] += 1
            continue

        source_zone_index = int(
            source_entities["zone_indices"][sample_index, entity_index].item()
        )
        source_zone_name = LOCATION_NAMES[source_zone_index]
        card = {
            "slot": len(zone["cards"]) + 1,
            "card_id": int(
                source_entities["card_ids"][sample_index, entity_index].item()
            ),
            "type": CARD_TYPE_NAMES.get(
                int(source_entities["card_types"][sample_index, entity_index].item()),
                "Unknown",
            ),
            "mana_cost": _mana_cost(
                source_entities["card_costs"][sample_index, entity_index]
            ),
            "attack": int(
                predicted_entities["card_atks"][sample_index, entity_index]
                .argmax(dim=-1)
                .item()
            ),
            "health": int(
                predicted_entities["card_hps"][sample_index, entity_index]
                .argmax(dim=-1)
                .item()
            ),
            "has_state": bool(
                torch.sigmoid(
                    predicted_entities["card_has_state"][sample_index, entity_index]
                ).item()
                >= 0.5
            ),
            "special_types": _special_types(
                predicted_entities["card_special_types"][sample_index, entity_index],
                logits=True,
            ),
            "source_zone": source_zone_name,
            "destination_zone": destination_name,
            "location_confidence": round(
                float(location_probs[entity_index, destination_index].item()),
                3,
            ),
            "presence_confidence": round(
                float(1.0 - location_probs[entity_index, -1].item()),
                3,
            ),
        }
        if destination_name in BOARD_ZONE_NAMES:
            card["tapped"] = bool(
                torch.sigmoid(
                    predicted_entities["card_tapped"][sample_index, entity_index]
                ).item()
                >= 0.5
            )
        zone["cards"].append(card)

    for _, zone in iter_entity_zones(display_state):
        zone["card_count"] = len(zone["cards"])
    return display_state


# ============================================================
# Per-card comparison and metrics
# ============================================================

def _attribute_summary(attack, health, has_state, tapped, tapped_valid):
    parts = []
    if has_state:
        parts.append(f"{attack}/{health}")
    if tapped_valid:
        parts.append("tapped" if tapped else "untapped")
    return " · ".join(parts) if parts else "—"


def entity_transition_rows(prediction, source, target, sample_index):
    """Return one source-card row with predicted and real destinations."""
    source_entities, aligned_target = align_next_entities(source, target)
    predicted_entities = flatten_entity_predictions(prediction)
    source_valid = source_entities["card_mask"][sample_index].bool()
    location_probs = F.softmax(
        predicted_entities["destination_zone"][sample_index],
        dim=-1,
    )
    predicted_zones = location_probs.argmax(dim=-1)

    rows = []
    for entity_index in torch.nonzero(source_valid, as_tuple=False).flatten().tolist():
        source_zone_index = int(
            source_entities["zone_indices"][sample_index, entity_index].item()
        )
        predicted_zone_index = int(predicted_zones[entity_index].item())
        target_zone_index = int(
            aligned_target["destination_zone"][sample_index, entity_index].item()
        )
        matched = bool(aligned_target["matched"][sample_index, entity_index].item())
        target_has_state = matched and bool(
            aligned_target["card_has_state"][sample_index, entity_index].item() >= 0.5
        )
        target_tapped_valid = matched and bool(
            aligned_target["card_tapped_valid"][
                sample_index,
                entity_index,
            ].item()
            >= 0.5
        )

        predicted_has_state = bool(
            torch.sigmoid(
                predicted_entities["card_has_state"][sample_index, entity_index]
            ).item()
            >= 0.5
        )
        predicted_tapped_valid = (
            LOCATION_NAMES[predicted_zone_index] in BOARD_ZONE_NAMES
        )
        rows.append(
            {
                "card_id": int(
                    source_entities["card_ids"][sample_index, entity_index].item()
                ),
                "card_type": CARD_TYPE_NAMES.get(
                    int(
                        source_entities["card_types"][
                            sample_index,
                            entity_index,
                        ].item()
                    ),
                    "Unknown",
                ),
                "source_zone": LOCATION_NAMES[source_zone_index],
                "predicted_zone": LOCATION_NAMES[predicted_zone_index],
                "target_zone": LOCATION_NAMES[target_zone_index],
                "confidence": round(
                    float(location_probs[entity_index, predicted_zone_index].item()),
                    3,
                ),
                "correct": predicted_zone_index == target_zone_index,
                "moved": source_zone_index != target_zone_index,
                "predicted_attributes": _attribute_summary(
                    int(
                        predicted_entities["card_atks"][sample_index, entity_index]
                        .argmax(dim=-1)
                        .item()
                    ),
                    int(
                        predicted_entities["card_hps"][sample_index, entity_index]
                        .argmax(dim=-1)
                        .item()
                    ),
                    predicted_has_state,
                    bool(
                        torch.sigmoid(
                            predicted_entities["card_tapped"][
                                sample_index,
                                entity_index,
                            ]
                        ).item()
                        >= 0.5
                    ),
                    predicted_tapped_valid,
                ),
                "target_attributes": _attribute_summary(
                    _normalized_stat(
                        aligned_target["card_atks"][sample_index, entity_index]
                    ),
                    _normalized_stat(
                        aligned_target["card_hps"][sample_index, entity_index]
                    ),
                    target_has_state,
                    matched and bool(
                        aligned_target["card_tapped"][sample_index, entity_index].item()
                        >= 0.5
                    ),
                    target_tapped_valid,
                ),
            }
        )

    # Movement and mistakes carry the most information in an ablation view.
    return sorted(
        rows,
        key=lambda row: (
            not row["moved"],
            row["correct"],
            row["source_zone"],
            row["card_id"],
        ),
    )


def _masked_mean(values, valid):
    if not valid.any():
        return values.float().new_zeros(())
    return values[valid].float().mean()


def entity_reconstruction_metrics(prediction, source, target, sample_index):
    """Compute compact per-sample diagnostics for the entity reconstruction."""
    source_entities, aligned_target = align_next_entities(source, target)
    predicted_entities = flatten_entity_predictions(prediction)

    pred_global = prediction["global_state"][sample_index]
    target_global = target["global_state"][sample_index]
    target_global_class = (
        target_global.float() * (pred_global.shape[-1] - 1)
    ).round().long().clamp(0, pred_global.shape[-1] - 1)
    global_ce = F.cross_entropy(pred_global, target_global_class)

    source_valid = source_entities["card_mask"][sample_index].bool()
    location_logits = predicted_entities["destination_zone"][sample_index]
    target_zone = aligned_target["destination_zone"][sample_index]
    location_ce = _masked_mean(
        F.cross_entropy(location_logits, target_zone, reduction="none"),
        source_valid,
    )
    predicted_zone = location_logits.argmax(dim=-1)
    location_correct = predicted_zone == target_zone
    location_accuracy = _masked_mean(location_correct, source_valid)

    moved_valid = source_valid & (
        target_zone != source_entities["zone_indices"][sample_index]
    )
    moved_accuracy = _masked_mean(location_correct, moved_valid)
    matched = source_valid & aligned_target["matched"][sample_index]
    matched_rate = _masked_mean(aligned_target["matched"][sample_index], source_valid)

    combat_valid = matched & aligned_target["card_has_state"][sample_index].bool()
    stat_mae = {}
    for field_name, metric_name in (
        ("card_atks", "attack_mae"),
        ("card_hps", "health_mae"),
    ):
        logits = predicted_entities[field_name][sample_index]
        target_class = (
            aligned_target[field_name][sample_index].float()
            * (logits.shape[-1] - 1)
        ).round().long().clamp(0, logits.shape[-1] - 1)
        stat_mae[metric_name] = _masked_mean(
            (logits.argmax(dim=-1) - target_class).abs(),
            combat_valid,
        )

    tapped_valid = matched & aligned_target["card_tapped_valid"][sample_index].bool()
    tapped_correct = (
        torch.sigmoid(predicted_entities["card_tapped"][sample_index]) >= 0.5
    ) == aligned_target["card_tapped"][sample_index].bool()
    tapped_accuracy = _masked_mean(tapped_correct, tapped_valid)

    score = (
        global_ce
        + location_ce
        + stat_mae["attack_mae"] / 20.0
        + stat_mae["health_mae"] / 20.0
        + torch.where(
            tapped_valid.any(),
            1.0 - tapped_accuracy,
            tapped_accuracy.new_zeros(()),
        )
    )

    def rounded(value):
        return round(float(value.detach().cpu().item()), 6)

    return {
        "global_ce": rounded(global_ce),
        "location_ce": rounded(location_ce),
        "location_accuracy": rounded(location_accuracy),
        "moved_location_accuracy": rounded(moved_accuracy),
        "moved_count": int(moved_valid.sum().detach().cpu().item()),
        "matched_card_rate": rounded(matched_rate),
        "attack_mae": rounded(stat_mae["attack_mae"]),
        "health_mae": rounded(stat_mae["health_mae"]),
        "tapped_accuracy": rounded(tapped_accuracy),
        "score": rounded(score),
    }
