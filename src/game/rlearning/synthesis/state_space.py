"""Convert state-space CVAE tensors into stable reconstruction artifacts."""

from __future__ import annotations

from collections import Counter
from typing import Any

import torch
import torch.nn.functional as F


CARD_TYPE_NAMES = {
    0: "Unknown",
    1: "Creature",
    2: "Instant",
    3: "Land",
    4: "Sorcery",
}

SPECIAL_TYPE_NAMES = {
    0: "ETB effect",
    1: "LTB effect",
    2: "Reach",
    3: "Trample",
    4: "Flying",
    5: "Haste",
    6: "Flash",
    7: "Lifelink",
    8: "Can attack",
    9: "Infect",
    10: "Indestructible",
}

MANA_NAMES = ["C", "U", "W", "B", "R", "G"]
# The original ``specific`` state predates the shared entity schema.  It
# stores only the five coloured mana values in U/R/G/W/B order.
LEGACY_MANA_NAMES = ["U", "R", "G", "W", "B"]


def _mana_names_for_global_width(global_width: int) -> list[str]:
    """Return the mana schema used by a global-state tensor.

    Entity states contain life x 2 plus six mana values (8 channels), while
    the original specific state contains life x 2 plus five coloured mana
    values (7 channels).
    """
    if global_width == 2 + len(MANA_NAMES):
        return MANA_NAMES
    if global_width == 2 + len(LEGACY_MANA_NAMES):
        return LEGACY_MANA_NAMES
    raise ValueError(
        "Unsupported global-state width: "
        f"expected 7 or 8 channels, got {global_width}"
    )


def describe_action(action_index: int) -> str:
    """Return the stable, context-free portion of the state-space action."""
    if action_index == 0:
        return "End turn"
    if action_index == 1:
        return "End response window"
    if 2 <= action_index <= 11:
        return f"Select attacker: battlefield slot {action_index - 1}"
    if 12 <= action_index <= 21:
        return f"Select blocker: battlefield slot {action_index - 11}"
    if 22 <= action_index <= 31:
        return f"Activate land ability: slot {action_index - 21}"
    if action_index >= 32:
        card_slot, sub_action = divmod(action_index - 32, 33)
        return f"Play hand card slot {card_slot + 1} (sub-action {sub_action})"
    return f"Unknown action {action_index}"


def _as_float(value: torch.Tensor) -> float:
    return float(value.detach().cpu().item())


def _clamped_integer(value: torch.Tensor | float, scale: float = 1.0) -> int:
    if isinstance(value, torch.Tensor):
        value = _as_float(value)
    return max(0, min(20, round(float(value) * scale)))


def _stat_class_from_logits(logits: torch.Tensor) -> int:
    """Decode discrete stat logits to their integer class."""
    return int(logits.argmax(dim=-1).detach().cpu().item())


def _normalized_values_to_classes(
    values: torch.Tensor,
    num_classes: int,
) -> torch.Tensor:
    return (values.float() * (num_classes - 1)).round().long().clamp(
        0,
        num_classes - 1,
    )


def _active_special_types(values: torch.Tensor, threshold: float | None) -> list[str]:
    values = values.detach().cpu()
    if threshold is None:
        active = torch.nonzero(values > 0.5, as_tuple=False).flatten().tolist()
    else:
        active = torch.nonzero(torch.sigmoid(values) >= threshold, as_tuple=False).flatten().tolist()
    return [SPECIAL_TYPE_NAMES.get(index, f"Trait {index}") for index in active]


def _mana_cost_from_target(values: torch.Tensor) -> list[int]:
    values = values.detach().cpu().flatten()
    return [_clamped_integer(value) for value in values]


def _mana_cost_from_prediction(logits: torch.Tensor) -> list[int]:
    return logits.detach().cpu().argmax(dim=-1).tolist()


def _card_from_target(zone: dict[str, torch.Tensor], slot_index: int, *, board: bool) -> dict[str, Any] | None:
    if _as_float(zone["card_mask"][slot_index]) <= 0.5:
        return None

    card: dict[str, Any] = {
        "slot": slot_index + 1,
        "type": "Creature" if board else CARD_TYPE_NAMES.get(
            int(_as_float(zone["card_types"][slot_index])), "Unknown"
        ),
        "attack": _clamped_integer(zone["card_atks"][slot_index], scale=20),
        "health": _clamped_integer(zone["card_hps"][slot_index], scale=20),
        "has_state": _as_float(zone["card_has_state"][slot_index]) > 0.5,
        "special_types": _active_special_types(zone["card_special_types"][slot_index], None),
        "presence_confidence": 1.0,
    }
    if not board:
        card["mana_cost"] = _mana_cost_from_target(
            zone["card_costs"][slot_index]
        )
    return card


def _card_from_prediction(zone: dict[str, torch.Tensor], slot_index: int, *, board: bool) -> dict[str, Any] | None:
    presence = torch.sigmoid(zone["card_mask"][slot_index])
    presence_value = _as_float(presence)
    if presence_value < 0.5:
        return None

    card: dict[str, Any] = {
        "slot": slot_index + 1,
        "type": "Creature" if board else CARD_TYPE_NAMES.get(
            int(zone["card_types"][slot_index].argmax().detach().cpu().item()), "Unknown"
        ),
        "attack": _stat_class_from_logits(zone["card_atks"][slot_index]),
        "health": _stat_class_from_logits(zone["card_hps"][slot_index]),
        "has_state": _as_float(torch.sigmoid(zone["card_has_state"][slot_index])) >= 0.5,
        "special_types": _active_special_types(zone["card_special_types"][slot_index], 0.5),
        "presence_confidence": round(presence_value, 3),
    }
    if not board:
        card["mana_cost"] = _mana_cost_from_prediction(
            zone["card_costs"][slot_index]
        )
    return card


def _zone_from_target(zone: dict[str, torch.Tensor], *, board: bool) -> dict[str, Any]:
    cards = [
        card
        for slot_index in range(zone["card_mask"].shape[0])
        if (card := _card_from_target(zone, slot_index, board=board)) is not None
    ]
    return {"card_count": len(cards), "slot_count": int(zone["card_mask"].shape[0]), "cards": cards}


def _zone_from_prediction(zone: dict[str, torch.Tensor], *, board: bool) -> dict[str, Any]:
    cards = [
        card
        for slot_index in range(zone["card_mask"].shape[0])
        if (card := _card_from_prediction(zone, slot_index, board=board)) is not None
    ]
    return {"card_count": len(cards), "slot_count": int(zone["card_mask"].shape[0]), "cards": cards}


def _select_zone_sample(
    zone: dict[str, torch.Tensor], sample_index: int
) -> dict[str, torch.Tensor]:
    """Remove the batch dimension from every tensor in one zone."""
    return {name: value[sample_index] for name, value in zone.items()}


def _global_from_target(values: torch.Tensor) -> dict[str, Any]:
    values = values.detach().cpu().flatten()
    mana_names = _mana_names_for_global_width(values.numel())
    mana_values = values[2 : 2 + len(mana_names)]
    return {
        "self_life": _clamped_integer(values[0], scale=20),
        "oppo_life": _clamped_integer(values[1], scale=20),
        "mana": {
            mana_name: _clamped_integer(value, scale=20)
            for mana_name, value in zip(mana_names, mana_values)
        },
    }


def _global_from_prediction(values: torch.Tensor) -> dict[str, Any]:
    """Decode discrete global class logits with shape [G, K]."""
    classes = values.detach().cpu().argmax(dim=-1).tolist()
    mana_names = _mana_names_for_global_width(len(classes))
    return {
        "self_life": classes[0],
        "oppo_life": classes[1],
        "mana": {
            mana_name: classes[2 + offset]
            for offset, mana_name in enumerate(mana_names)
        },
    }


def _stack_context(state: dict[str, Any], sample_index: int) -> dict[int, dict[str, Any]]:
    """Extract the non-card metadata associated with stack slots when present."""
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
        has_player = _as_float(player.max()) > 0.5
        if not has_player and _as_float(actions[slot_index]) == 0:
            continue
        if not has_player:
            player_name = "Unknown"
        else:
            player_name = "Self" if int(player.argmax().item()) == 0 else "Opponent"
        context[slot_index] = {
            "stack_player": player_name,
            "stack_action": int(_as_float(actions[slot_index])),
        }
    return context


def state_from_target(state: dict[str, Any], sample_index: int) -> dict[str, Any]:
    """Create the UI representation for a source or real next state."""
    display_state = {
        "global_state": _global_from_target(state["global_state"][sample_index]),
        "card_zones": {
            name: _zone_from_target(
                _select_zone_sample(zone, sample_index),
                board=False,
            )
            for name, zone in state["card_zones"].items()
        },
        "board_zones": {
            name: _zone_from_target(
                _select_zone_sample(zone, sample_index),
                board=True,
            )
            for name, zone in state["board_zones"].items()
        },
    }
    stack_context = _stack_context(state, sample_index)
    for card in display_state["card_zones"]["stack_cards"]["cards"]:
        card.update(stack_context.get(card["slot"] - 1, {}))
    return display_state


def state_from_prediction(prediction: dict[str, Any], sample_index: int) -> dict[str, Any]:
    """Turn decoder logits into the thresholded display state."""
    return {
        "global_state": _global_from_prediction(prediction["global_state"][sample_index]),
        "card_zones": {
            name: _zone_from_prediction(
                _select_zone_sample(zone, sample_index),
                board=False,
            )
            for name, zone in prediction["card_zones"].items()
        },
        "board_zones": {
            name: _zone_from_prediction(
                _select_zone_sample(zone, sample_index),
                board=True,
            )
            for name, zone in prediction["board_zones"].items()
        },
    }


def _card_state_signature(card: dict[str, Any]) -> tuple[Any, ...]:
    """Return the comparable, model-independent part of one rendered card."""
    special_types = card.get("special_types", ())
    if isinstance(special_types, str):
        special_types = (special_types,)
    else:
        special_types = tuple(sorted(str(value) for value in special_types))

    mana_cost = card.get("mana_cost", ())
    if isinstance(mana_cost, str):
        mana_cost = (mana_cost,)
    else:
        mana_cost = tuple(mana_cost)

    # Card IDs are intentionally excluded: source-aligned decoders know the
    # IDs of existing cards, while birth-query decoders produce virtual IDs.
    # The zone and rendered card state are the common representation shared by
    # all reconstruction outputs.
    return (
        str(card.get("type", "Unknown")),
        mana_cost,
        int(card.get("attack", 0)),
        int(card.get("health", 0)),
        bool(card.get("has_state", False)),
        special_types,
        bool(card.get("tapped", False)),
    )


def _state_card_counter(state: dict[str, Any]) -> Counter:
    cards = Counter()
    for collection in ("card_zones", "board_zones"):
        for zone_name, zone in state.get(collection, {}).items():
            for card in zone.get("cards", ()):
                cards[(collection, zone_name, _card_state_signature(card))] += 1
    return cards


def state_reconstruction_metrics(
    predicted_state: dict[str, Any],
    target_state: dict[str, Any],
) -> dict[str, float | int]:
    """Score rendered next states with one common evaluator for all models.

    The comparison is deliberately performed after decoding, rather than on
    model-specific logits. Cards are treated as an unordered multiset inside
    each zone, so source-aligned, birth-slot, and slot-based decoders share the
    same score definition.
    """
    predicted_global = predicted_state.get("global_state", {})
    target_global = target_state.get("global_state", {})
    predicted_mana = predicted_global.get("mana", {})
    target_mana = target_global.get("mana", {})
    mana_names = sorted(set(predicted_mana) | set(target_mana))
    global_values = [
        (predicted_global.get("self_life", 0), target_global.get("self_life", 0)),
        (predicted_global.get("oppo_life", 0), target_global.get("oppo_life", 0)),
    ]
    global_values.extend(
        (predicted_mana.get(name, 0), target_mana.get(name, 0))
        for name in mana_names
    )
    global_mae = (
        sum(
            abs(float(predicted) - float(target)) / 20.0
            for predicted, target in global_values
        )
        / max(len(global_values), 1)
    )

    predicted_cards = _state_card_counter(predicted_state)
    target_cards = _state_card_counter(target_state)
    predicted_count = sum(predicted_cards.values())
    target_count = sum(target_cards.values())
    intersection = sum((predicted_cards & target_cards).values())
    union = predicted_count + target_count - intersection
    card_set_jaccard = intersection / union if union else 1.0
    card_set_error = 1.0 - card_set_jaccard

    return {
        "global_mae": round(global_mae, 6),
        "card_set_jaccard": round(card_set_jaccard, 6),
        "card_set_error": round(card_set_error, 6),
        "predicted_card_count": predicted_count,
        "target_card_count": target_count,
        "score": round(global_mae + card_set_error, 6),
    }


def _count_zone_cards(state: dict[str, Any], collection: str, name: str, sample_index: int) -> int:
    zone = state.get(collection, {}).get(name)
    if not isinstance(zone, dict) or "card_mask" not in zone:
        return 0
    mask = zone["card_mask"][sample_index].detach().cpu().float()
    return int((mask > 0.5).sum().item())


def _target_life(state: dict[str, Any], sample_index: int, offset: int) -> int:
    return _clamped_integer(state["global_state"][sample_index].flatten()[offset], scale=20)


def _target_mana_total(state: dict[str, Any], sample_index: int) -> int:
    values = state["global_state"][sample_index].detach().cpu().flatten()
    mana_names = _mana_names_for_global_width(values.numel())
    return sum(
        _clamped_integer(value, scale=20)
        for value in values[2 : 2 + len(mana_names)]
    )


def state_delta_from_target(source: dict[str, Any], target: dict[str, Any], sample_index: int) -> dict[str, Any]:
    """Summarize the real state change for coloring transition points."""
    self_life_delta = _target_life(target, sample_index, 0) - _target_life(source, sample_index, 0)
    oppo_life_delta = _target_life(target, sample_index, 1) - _target_life(source, sample_index, 1)
    hand_delta = _count_zone_cards(target, "card_zones", "hand", sample_index) - _count_zone_cards(source, "card_zones", "hand", sample_index)
    graveyard_delta = _count_zone_cards(target, "card_zones", "graveyard", sample_index) - _count_zone_cards(source, "card_zones", "graveyard", sample_index)
    library_delta = _count_zone_cards(target, "card_zones", "library", sample_index) - _count_zone_cards(source, "card_zones", "library", sample_index)
    self_board_delta = _count_zone_cards(target, "board_zones", "self_board", sample_index) - _count_zone_cards(source, "board_zones", "self_board", sample_index)
    oppo_board_delta = _count_zone_cards(target, "board_zones", "oppo_board", sample_index) - _count_zone_cards(source, "board_zones", "oppo_board", sample_index)
    mana_delta = _target_mana_total(target, sample_index) - _target_mana_total(source, sample_index)

    change_type = "no_major_change"
    if oppo_life_delta < 0:
        change_type = "opponent_damage"
    elif self_life_delta < 0:
        change_type = "self_damage"
    elif self_life_delta > 0 or oppo_life_delta > 0:
        change_type = "life_gain"
    elif self_board_delta > 0 or oppo_board_delta > 0:
        change_type = "summon"
    elif self_board_delta < 0 or oppo_board_delta < 0:
        change_type = "remove"
    elif hand_delta > 0:
        change_type = "draw"
    elif hand_delta < 0:
        change_type = "discard"
    elif graveyard_delta != 0:
        change_type = "graveyard_change"
    elif library_delta != 0:
        change_type = "library_change"
    elif mana_delta != 0:
        change_type = "mana_change"

    return {
        "change_type": change_type,
        "self_life_delta": self_life_delta,
        "oppo_life_delta": oppo_life_delta,
        "hand_delta": hand_delta,
        "graveyard_delta": graveyard_delta,
        "library_delta": library_delta,
        "self_board_delta": self_board_delta,
        "oppo_board_delta": oppo_board_delta,
        "mana_delta": mana_delta,
    }


def card_used_from_raw(card_used: dict[str, Any] | None) -> dict[str, Any]:
    """Format the raw card data retained by the replay dataset."""
    card_used = card_used or {}
    special_types = card_used.get("special_type", [])
    if isinstance(special_types, torch.Tensor):
        special_types = special_types.detach().cpu().tolist()

    active = [
        SPECIAL_TYPE_NAMES.get(index, f"Trait {index}")
        for index, value in enumerate(special_types)
        if float(value) > 0.5
    ]
    mana_cost = card_used.get("mana_cost", [])
    if isinstance(mana_cost, torch.Tensor):
        mana_cost = mana_cost.detach().cpu().tolist()

    card_type = card_used.get("card_type", 0)
    if isinstance(card_type, torch.Tensor):
        card_type = int(card_type.detach().cpu().item())

    colors = card_used.get("color_identity", [])
    if isinstance(colors, torch.Tensor):
        colors = colors.detach().cpu().tolist()
    return {
        "description": str(card_used.get("description", "No card text available")),
        "type": CARD_TYPE_NAMES.get(int(card_type), "Unknown"),
        "mana_cost": [_clamped_integer(value, scale=20) for value in mana_cost],
        "colors": [name for name, value in zip(MANA_NAMES[1:], colors) if float(value) > 0.5],
        "attack": _clamped_integer(card_used.get("attack", 0), scale=20),
        "health": _clamped_integer(card_used.get("defend", 0), scale=20),
        "has_state": bool(card_used.get("has_state", False)),
        "special_types": active,
    }


def reconstruction_metrics(
    prediction: dict[str, Any], target: dict[str, Any], sample_index: int
) -> dict[str, float]:
    """Small per-sample diagnostics for the reconstruction list."""
    pred_global = prediction["global_state"][sample_index]
    target_global = target["global_state"][sample_index]
    target_classes = _normalized_values_to_classes(
        target_global,
        pred_global.shape[-1],
    )
    global_ce = F.cross_entropy(pred_global, target_classes)

    mask_losses = []
    for collection in ("card_zones", "board_zones"):
        for name, pred_zone in prediction[collection].items():
            target_mask = target[collection][name]["card_mask"].float()
            mask_losses.append(
                F.binary_cross_entropy_with_logits(
                    pred_zone["card_mask"][sample_index], target_mask[sample_index]
                )
            )

    mask_bce = torch.stack(mask_losses).mean()
    total = global_ce + mask_bce
    return {
        "global_ce": round(_as_float(global_ce), 6),
        "mask_bce": round(_as_float(mask_bce), 6),
        "score": round(_as_float(total), 6),
    }
