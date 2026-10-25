"""Compute a bounded base score from resources, board strength, mana, and life."""

from __future__ import annotations

from math import exp, isfinite, tanh
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from game.player import Player
    from game.room import Room
    from game.type_cards.creature import Creature


def get_reward(
    room: Room,
    agent: Player,
    battled_creature: Optional[Creature] = None,
    attacker: Optional[Creature] = None,
) -> dict:
    """Return base_score under the legacy reward key, with replay-compatible details.

    Scores depend only on the current state; combat arguments are kept for compatibility.
    Terminal scores describe outcomes, including projected ones. The training room must
    separately set terminal potentials to zero when computing the final training reward.
    """
    config = getattr(agent, "config", getattr(room, "config", {}))
    parameters = _parameters(config.get("reward", {}))
    own = _player_values(room, agent, parameters)
    opponent = _player_values(room, agent.opponent, parameters)
    advantages = {
        "resource": tanh((own["assets"] - opponent["assets"]) / parameters["resource_scale"]),
        "board": tanh((own["board"] - opponent["board"]) / parameters["board_scale"]),
        "mana": own["mana"] - opponent["mana"],
        "life": own["life"] - opponent["life"],
    }
    weight_sum = sum(parameters[f"{name}_weight"] for name in advantages)
    if not isfinite(weight_sum) or weight_sum <= 0:
        raise ValueError("Component weights must have a finite positive sum")
    base_score = sum(parameters[f"{name}_weight"] * value for name, value in advantages.items()) / weight_sum
    terminal = own["dead"] or opponent["dead"]
    if terminal:
        base_score = float(opponent["dead"]) - float(own["dead"])
    return {
        "reward": base_score,
        "base_score": base_score,
        "terminal": terminal,
        "resource_advantage": advantages["resource"],
        "board_advantage": advantages["board"],
        "mana_advantage": advantages["mana"],
        "life_advantage": advantages["life"],
        "assets_self": own["assets"],
        "assets_oppo": opponent["assets"],
        "mana_capacity_self": own["mana_capacity"],
        "mana_capacity_oppo": opponent["mana_capacity"],
        "score_life_self": own["life"],
        "score_oppo_self": opponent["life"],
        "score_mana": own["mana"],
        "score_hand": len(agent.hand) / 30.0,  # Legacy display field, not used in base_score.
        "score_battle_self": own["board"],
        "score_battle_oppo": opponent["board"],
        "score_battle_self_creatures": own["creatures"],
        "score_battle_oppo_creatures": opponent["creatures"],
    }


def _parameters(config: dict) -> dict[str, float]:
    defaults = {
        "resource_weight": 0.10,
        "board_weight": 0.325,
        "mana_weight": 0.10,
        "life_weight": 0.455,
        "resource_scale": 6.0,
        "board_scale": 8.0,
        "mana_scale": 6.0,
        "life_scale": 8.0,
        "power_weight": 0.50,
        "health_weight": 0.25,
    }
    parameters = {name: float(config.get(name, default)) for name, default in defaults.items()}
    for name, value in parameters.items():
        if not isfinite(value) or value < 0 or (name.endswith("_scale") and value == 0):
            raise ValueError(f"Invalid reward parameter {name}: {value}")
    return parameters


def _player_values(room: Room, player: Player, parameters: dict[str, float]) -> dict:
    assets = {id(card) for card in player.hand}
    creature_values = []
    for card in player.battlefield:
        power, health = card.state
        active = health > 0 and not card.get_flag("die") and not card.get_flag("exile")
        value = parameters["power_weight"] * max(0.0, float(power))
        value += parameters["health_weight"] * max(0.0, float(health))
        creature_values.append(value if active else 0.0)
        if active:
            assets.add(id(card))
    mana_capacity = 0.0
    for land in player.land_area:
        if land.get_flag("die") or land.get_flag("exile"):
            continue
        assets.add(id(land))
        mana_capacity += float(sum(land.generate_mana().values()))
    assets.update(id(item["card"]) for item in room.stack if item["card"].player is player)
    return {
        "assets": len(assets),
        "board": sum(creature_values),
        "creatures": creature_values,
        "mana_capacity": max(0.0, mana_capacity),
        "mana": _utility(mana_capacity, parameters["mana_scale"]),
        "life": _utility(player.life, parameters["life_scale"]),
        "dead": bool(player.life <= 0 or player.get_flag("die")),
    }


def _utility(value: float, scale: float) -> float:
    """Apply diminishing returns to nonnegative mana capacity or life."""
    return 1.0 - exp(-max(0.0, float(value)) / scale)
