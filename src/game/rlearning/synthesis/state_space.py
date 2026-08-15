"""Convert state-space CVAE tensors into stable reconstruction artifacts."""

from __future__ import annotations

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

MANA_NAMES = ["U", "R", "G", "W", "B"]


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


def _active_special_types(values: torch.Tensor, threshold: float | None) -> list[str]:
    values = values.detach().cpu()
    if threshold is None:
        active = torch.nonzero(values > 0.5, as_tuple=False).flatten().tolist()
    else:
        active = torch.nonzero(torch.sigmoid(values) >= threshold, as_tuple=False).flatten().tolist()
    return [SPECIAL_TYPE_NAMES.get(index, f"Trait {index}") for index in active]


def _mana_cost(values: torch.Tensor) -> list[int]:
    values = values.detach().cpu().flatten()
    return [_clamped_integer(value) for value in values]


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
        card["mana_cost"] = _mana_cost(zone["card_costs"][slot_index])
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
        "attack": _clamped_integer(zone["card_atks"][slot_index], scale=20),
        "health": _clamped_integer(zone["card_hps"][slot_index], scale=20),
        "has_state": _as_float(torch.sigmoid(zone["card_has_state"][slot_index])) >= 0.5,
        "special_types": _active_special_types(zone["card_special_types"][slot_index], 0.5),
        "presence_confidence": round(presence_value, 3),
    }
    if not board:
        card["mana_cost"] = _mana_cost(zone["card_costs"][slot_index])
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
    mana_values = values[2 : 2 + len(MANA_NAMES)]
    return {
        "self_life": _clamped_integer(values[0], scale=20),
        "oppo_life": _clamped_integer(values[1], scale=20),
        "mana": {
            mana_name: _clamped_integer(value, scale=20)
            for mana_name, value in zip(MANA_NAMES, mana_values)
        },
    }


def _global_from_prediction(values: torch.Tensor) -> dict[str, Any]:
    values = values.detach().cpu().flatten()
    mana_values = values[2 : 2 + len(MANA_NAMES)]
    return {
        "self_life": _clamped_integer(values[0], scale=20),
        "oppo_life": _clamped_integer(values[1], scale=20),
        "mana": {
            mana_name: _clamped_integer(value, scale=20)
            for mana_name, value in zip(MANA_NAMES, mana_values)
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

    return {
        "description": str(card_used.get("description", "No card text available")),
        "type": CARD_TYPE_NAMES.get(int(card_type), "Unknown"),
        "mana_cost": [_clamped_integer(value, scale=20) for value in mana_cost],
        "attack": _clamped_integer(card_used.get("attack", 0), scale=20),
        "health": _clamped_integer(card_used.get("defend", 0), scale=20),
        "has_state": bool(card_used.get("has_state", False)),
        "special_types": active,
    }


def reconstruction_metrics(
    prediction: dict[str, Any], target: dict[str, Any], sample_index: int
) -> dict[str, float]:
    """Small per-sample diagnostics for the reconstruction list."""
    global_mse = F.mse_loss(
        prediction["global_state"][sample_index], target["global_state"][sample_index]
    )

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
    total = global_mse + mask_bce
    return {
        "global_mse": round(_as_float(global_mse), 6),
        "mask_bce": round(_as_float(mask_bce), 6),
        "score": round(_as_float(total), 6),
    }
