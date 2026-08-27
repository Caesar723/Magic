"""Birth-slot matching and visualization helpers for entity transitions."""

from __future__ import annotations

from typing import Any

import torch
import torch.nn.functional as F

from game.rlearning.states.state_space.specific_entity import (
    BOARD_ZONE_NAMES,
    CARD_ZONE_NAMES,
    LOCATION_NAMES,
)
from game.rlearning.synthesis.entity_transition import (
    _attribute_summary,
    _gather_slots,
    _mana_cost,
    _normalized_stat,
    _special_types,
    entity_reconstruction_metrics,
    entity_transition_rows,
    flatten_state_entities,
    state_from_entity_prediction,
)
from game.rlearning.synthesis.state_space import CARD_TYPE_NAMES


def unmatched_target_entities(source, target):
    """Return flattened next-state entities that have no source instance.

    This intentionally mirrors source alignment in ``align_next_entities`` so
    movements represented by a shared instance ID are not treated as births.
    """
    source_entities = flatten_state_entities(source)
    target_entities = flatten_state_entities(target)
    source_valid = source_entities["card_mask"].bool()
    target_valid = target_entities["card_mask"].bool()

    id_matches = (
        source_entities["card_ids"].unsqueeze(-1)
        == target_entities["card_ids"].unsqueeze(1)
    ) & source_valid.unsqueeze(-1) & target_valid.unsqueeze(1)
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
    target_is_existing = preferred_matches.any(dim=1)
    return target_entities, target_valid & ~target_is_existing


def _value_classes(values, num_classes, value_scale):
    return (
        values.float() * value_scale
    ).round().long().clamp(0, num_classes - 1)


def _bce_cost(logits, target):
    """Pairwise BCE cost for query logits [Q, D] and targets [T, D]."""
    query_count, target_count = logits.shape[0], target.shape[0]
    return F.binary_cross_entropy_with_logits(
        logits[:, None, :].expand(query_count, target_count, -1),
        target[None, :, :].expand(query_count, target_count, -1),
        reduction="none",
    ).mean(dim=-1)


def _classification_cost(logits, target_classes):
    """Pairwise negative log likelihood for [Q, C] logits and [T] labels."""
    return -F.log_softmax(logits, dim=-1)[:, target_classes]


def birth_matching_cost(prediction, target_entities, batch_index, target_indices):
    """Build a detached assignment cost for one sample's birth queries."""
    num_stats = prediction["card_atks"].shape[-1]
    target_indices = target_indices.long()
    destination = target_entities["zone_indices"][batch_index, target_indices]
    card_types = target_entities["card_types"][batch_index, target_indices].long()
    attacks = _value_classes(
        target_entities["card_atks"][batch_index, target_indices],
        num_stats,
        num_stats - 1,
    )
    healths = _value_classes(
        target_entities["card_hps"][batch_index, target_indices],
        num_stats,
        num_stats - 1,
    )

    # Strongly prefer a slot whose categorical entity description agrees with
    # the target.  The assignment itself is detached; gradients come from the
    # losses after target-to-query matching, as in DETR-style set prediction.
    cost = 2.0 * _classification_cost(
        prediction["destination_zone"][batch_index],
        destination,
    )
    presence_cost = F.softplus(-prediction["presence"][batch_index])
    cost = cost + presence_cost[:, None].expand_as(cost)
    cost = cost + _classification_cost(
        prediction["card_types"][batch_index],
        card_types,
    )
    target_costs = target_entities["card_costs"][batch_index, target_indices]
    card_cost_cost = cost.new_zeros(cost.shape)
    for cost_index in range(target_costs.shape[-1]):
        cost_class = _value_classes(
            target_costs[:, cost_index],
            num_stats,
            1.0,
        )
        card_cost_cost = card_cost_cost + _classification_cost(
            prediction["card_costs"][batch_index, :, cost_index],
            cost_class,
        )
    cost = cost + 0.25 * card_cost_cost / target_costs.shape[-1]
    cost = cost + 0.5 * _classification_cost(
        prediction["card_atks"][batch_index],
        attacks,
    )
    cost = cost + 0.5 * _classification_cost(
        prediction["card_hps"][batch_index],
        healths,
    )
    cost = cost + _bce_cost(
        prediction["card_special_types"][batch_index],
        target_entities["card_special_types"][batch_index, target_indices],
    )

    has_state_target = target_entities["card_has_state"][batch_index, target_indices]
    has_state_logits = prediction["card_has_state"][batch_index][:, None]
    cost = cost + F.binary_cross_entropy_with_logits(
        has_state_logits.expand_as(cost),
        has_state_target[None, :].expand_as(cost),
        reduction="none",
    )

    tapped_valid = target_entities["card_tapped_valid"][batch_index, target_indices]
    tapped_target = target_entities["card_tapped"][batch_index, target_indices]
    tapped_logits = prediction["card_tapped"][batch_index][:, None]
    tapped_cost = F.binary_cross_entropy_with_logits(
        tapped_logits.expand_as(cost),
        tapped_target[None, :].expand_as(cost),
        reduction="none",
    )
    return (cost + tapped_cost * tapped_valid[None, :]).detach()


def _hungarian_minimum_assignment(cost: torch.Tensor) -> list[int]:
    """Assign every cost row to a distinct column with the Hungarian method.

    ``cost`` must have at most as many rows as columns.  The matrices here are
    tiny (at most ten birth targets), so a compact CPU implementation avoids a
    SciPy runtime dependency.
    """
    rows, columns = cost.shape
    if rows > columns:
        raise ValueError("Hungarian assignment requires rows <= columns.")
    matrix = cost.detach().float().cpu().tolist()
    u = [0.0] * (rows + 1)
    v = [0.0] * (columns + 1)
    p = [0] * (columns + 1)
    way = [0] * (columns + 1)

    for row in range(1, rows + 1):
        p[0] = row
        column0 = 0
        min_values = [float("inf")] * (columns + 1)
        used = [False] * (columns + 1)
        while True:
            used[column0] = True
            row0 = p[column0]
            delta = float("inf")
            next_column = 0
            for column in range(1, columns + 1):
                if used[column]:
                    continue
                current = matrix[row0 - 1][column - 1] - u[row0] - v[column]
                if current < min_values[column]:
                    min_values[column] = current
                    way[column] = column0
                if min_values[column] < delta:
                    delta = min_values[column]
                    next_column = column
            for column in range(columns + 1):
                if used[column]:
                    u[p[column]] += delta
                    v[column] -= delta
                else:
                    min_values[column] -= delta
            column0 = next_column
            if p[column0] == 0:
                break
        while True:
            previous_column = way[column0]
            p[column0] = p[previous_column]
            column0 = previous_column
            if column0 == 0:
                break

    assignment = [-1] * rows
    for column in range(1, columns + 1):
        if p[column]:
            assignment[p[column] - 1] = column - 1
    return assignment


def align_birth_slots(prediction, source, target):
    """Match unmatched target entities to unordered predicted birth slots.

    If a sample has more new entities than configured slots, only the first
    ``num_birth_slots`` in stable flattened-zone order are supervised and the
    remaining count is returned as ``overflow_count`` for monitoring.
    """
    target_entities, unmatched = unmatched_target_entities(source, target)
    presence = prediction["presence"]
    batch_size, num_slots = presence.shape
    device = presence.device
    selected_indices = torch.zeros(
        batch_size,
        num_slots,
        dtype=torch.long,
        device=device,
    )
    slot_matched = torch.zeros(
        batch_size,
        num_slots,
        dtype=torch.bool,
        device=device,
    )
    target_counts = torch.zeros(batch_size, dtype=torch.long, device=device)
    overflow_counts = torch.zeros_like(target_counts)
    candidate_indices = []
    padded_costs = []

    for batch_index in range(batch_size):
        target_indices = torch.nonzero(
            unmatched[batch_index],
            as_tuple=False,
        ).flatten()
        target_counts[batch_index] = target_indices.numel()
        if target_indices.numel() == 0:
            candidate_indices.append(target_indices)
            padded_costs.append(
                presence.new_zeros(num_slots, num_slots)
            )
            continue
        if target_indices.numel() > num_slots:
            overflow_counts[batch_index] = target_indices.numel() - num_slots
            target_indices = target_indices[:num_slots]
        candidate_indices.append(target_indices)
        # Hungarian rows are targets and columns are the learned birth queries.
        # Pad before the device transfer so an entire batch synchronizes only
        # once instead of once per sample.
        cost = birth_matching_cost(
            prediction,
            target_entities,
            batch_index,
            target_indices,
        ).transpose(0, 1)
        padded_cost = presence.new_zeros(num_slots, num_slots)
        padded_cost[: target_indices.numel()] = cost
        padded_costs.append(padded_cost)

    all_costs = torch.stack(padded_costs).detach().float().cpu()
    for batch_index, target_indices in enumerate(candidate_indices):
        if target_indices.numel() == 0:
            continue
        assignment = _hungarian_minimum_assignment(
            all_costs[batch_index, : target_indices.numel()]
        )
        assigned_slots = torch.as_tensor(
            assignment,
            dtype=torch.long,
            device=device,
        )
        selected_indices[batch_index, assigned_slots] = target_indices
        slot_matched[batch_index, assigned_slots] = True

    aligned = {
        field_name: _gather_slots(values, selected_indices)
        for field_name, values in target_entities.items()
    }
    aligned["destination_zone"] = aligned.pop("zone_indices")
    aligned["matched"] = slot_matched
    aligned["target_count"] = target_counts
    aligned["overflow_count"] = overflow_counts
    return aligned


def state_from_entity_birth_prediction(prediction, source, sample_index):
    """Render source-card predictions and append selected virtual births."""
    display_state = state_from_entity_prediction(prediction, source, sample_index)
    births = prediction["births"]
    presence = torch.sigmoid(births["presence"][sample_index]) >= 0.5
    destinations = births["destination_zone"][sample_index].argmax(dim=-1)

    for slot_index in torch.nonzero(presence, as_tuple=False).flatten().tolist():
        destination_index = int(destinations[slot_index].item())
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

        card: dict[str, Any] = {
            "slot": len(zone["cards"]) + 1,
            "card_id": f"birth-{slot_index + 1}",
            "type": CARD_TYPE_NAMES.get(
                int(births["card_types"][sample_index, slot_index].argmax().item()),
                "Unknown",
            ),
            "mana_cost": _mana_cost(
                births["card_costs"][sample_index, slot_index].argmax(dim=-1)
            ),
            "attack": int(
                births["card_atks"][sample_index, slot_index].argmax().item()
            ),
            "health": int(
                births["card_hps"][sample_index, slot_index].argmax().item()
            ),
            "has_state": bool(
                torch.sigmoid(
                    births["card_has_state"][sample_index, slot_index]
                ).item()
                >= 0.5
            ),
            "special_types": _special_types(
                births["card_special_types"][sample_index, slot_index],
                logits=True,
            ),
            "source_zone": "birth",
            "destination_zone": destination_name,
            "presence_confidence": round(
                float(torch.sigmoid(births["presence"][sample_index, slot_index]).item()),
                3,
            ),
        }
        if destination_name in BOARD_ZONE_NAMES:
            card["tapped"] = bool(
                torch.sigmoid(births["card_tapped"][sample_index, slot_index]).item()
                >= 0.5
            )
        zone["cards"].append(card)

    for collection in ("card_zones", "board_zones"):
        for zone in display_state[collection].values():
            zone["card_count"] = len(zone["cards"])
    return display_state


def entity_birth_transition_rows(prediction, source, target, sample_index):
    """Include ordinary source-card rows plus decoded birth-slot rows."""
    rows = entity_transition_rows(prediction, source, target, sample_index)
    births = prediction["births"]
    aligned = align_birth_slots(births, source, target)
    presence = torch.sigmoid(births["presence"][sample_index]) >= 0.5
    predicted_zones = births["destination_zone"][sample_index].argmax(dim=-1)
    location_probs = F.softmax(
        births["destination_zone"][sample_index],
        dim=-1,
    )
    outside_index = LOCATION_NAMES.index("outside")

    for slot_index in torch.nonzero(presence, as_tuple=False).flatten().tolist():
        matched = bool(aligned["matched"][sample_index, slot_index].item())
        predicted_zone_index = int(predicted_zones[slot_index].item())
        target_zone_index = (
            int(aligned["destination_zone"][sample_index, slot_index].item())
            if matched
            else outside_index
        )
        predicted_has_state = bool(
            torch.sigmoid(
                births["card_has_state"][sample_index, slot_index]
            ).item()
            >= 0.5
        )
        target_has_state = matched and bool(
            aligned["card_has_state"][sample_index, slot_index].item() >= 0.5
        )
        target_tapped_valid = matched and bool(
            aligned["card_tapped_valid"][sample_index, slot_index].item() >= 0.5
        )
        rows.append(
            {
                "card_id": f"birth-{slot_index + 1}",
                "card_type": CARD_TYPE_NAMES.get(
                    int(births["card_types"][sample_index, slot_index].argmax().item()),
                    "Unknown",
                ),
                "source_zone": "birth",
                "predicted_zone": LOCATION_NAMES[predicted_zone_index],
                "target_zone": LOCATION_NAMES[target_zone_index],
                "confidence": round(
                    float(location_probs[slot_index, predicted_zone_index].item()),
                    3,
                ),
                "correct": matched and predicted_zone_index == target_zone_index,
                "moved": True,
                "predicted_attributes": _attribute_summary(
                    int(births["card_atks"][sample_index, slot_index].argmax().item()),
                    int(births["card_hps"][sample_index, slot_index].argmax().item()),
                    predicted_has_state,
                    LOCATION_NAMES[predicted_zone_index] in BOARD_ZONE_NAMES
                    and bool(
                        torch.sigmoid(
                            births["card_tapped"][sample_index, slot_index]
                        ).item()
                        >= 0.5
                    ),
                    LOCATION_NAMES[predicted_zone_index] in BOARD_ZONE_NAMES,
                ),
                "target_attributes": _attribute_summary(
                    _normalized_stat(aligned["card_atks"][sample_index, slot_index])
                    if matched
                    else 0,
                    _normalized_stat(aligned["card_hps"][sample_index, slot_index])
                    if matched
                    else 0,
                    target_has_state,
                    matched
                    and bool(
                        aligned["card_tapped"][sample_index, slot_index].item() >= 0.5
                    ),
                    target_tapped_valid,
                ),
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            row["source_zone"] != "birth",
            not row["moved"],
            row["correct"],
            row["source_zone"],
            str(row["card_id"]),
        ),
    )


def entity_birth_reconstruction_metrics(prediction, source, target, sample_index):
    """Extend source-card reconstruction metrics with birth-count diagnostics."""
    metrics = entity_reconstruction_metrics(prediction, source, target, sample_index)
    births = prediction["births"]
    aligned = align_birth_slots(births, source, target)
    matched = aligned["matched"][sample_index]
    presence_target = matched.float()
    presence_bce = F.binary_cross_entropy_with_logits(
        births["presence"][sample_index],
        presence_target,
    )
    predicted_count = int(
        (torch.sigmoid(births["presence"][sample_index]) >= 0.5).sum().item()
    )
    target_count = int(aligned["target_count"][sample_index].item())
    overflow_count = int(aligned["overflow_count"][sample_index].item())
    if matched.any():
        destination_accuracy = float(
            (
                births["destination_zone"][sample_index].argmax(dim=-1)[matched]
                == aligned["destination_zone"][sample_index][matched]
            ).float().mean().item()
        )
    else:
        destination_accuracy = 0.0

    metrics["birth_presence_bce"] = round(float(presence_bce.item()), 6)
    metrics["birth_predicted_count"] = predicted_count
    metrics["birth_target_count"] = target_count
    metrics["birth_overflow_count"] = overflow_count
    metrics["birth_destination_accuracy"] = round(destination_accuracy, 6)
    metrics["score"] = round(
        metrics["score"]
        + float(presence_bce.item())
        + (1.0 - destination_accuracy if target_count else 0.0),
        6,
    )
    return metrics
