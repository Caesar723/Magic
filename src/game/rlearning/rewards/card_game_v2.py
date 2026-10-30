"""Bounded material score plus conservative one-attack tactical evaluation."""

from __future__ import annotations

from math import exp, isfinite, sqrt
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from game.player import Player
    from game.room import Room
    from game.type_cards.creature import Creature


_FLAGS = (
    "flying",
    "reach",
    "unblockable",
    "Menace",
    "Hexproof",
    "lifelink",
    "Trample",
    "Vigilance",
    "Double strike",
    "haste",
    "tap",
    "summoning_sickness",
)

_COMBAT_HOOKS = (
    "when_start_attcak",
    "when_start_defend",
    "when_finish_attcak",
    "when_finish_defend",
    "when_harm_is_done",
    "when_hurt",
    "when_die",
    "when_become_attacker",
    "when_kill_creature",
    "when_a_creature_die",
    "when_an_object_hert",
)


def get_reward(
    room: Room,
    agent: Player,
    battled_creature: Optional[Creature] = None,
    attacker: Optional[Creature] = None,
) -> dict:
    config = getattr(agent, "config", getattr(room, "config", {}))
    parameters = _parameters(config.get("reward", {}))

    reserved = _reserved_cards(room)
    own = _player_values(room, agent, parameters, reserved)
    opponent = _player_values(
        room, agent.opponent, parameters, reserved
    )

    material = _advantage(
        own["board"] - opponent["board"],
        parameters["board_scale"],
    )

    combat_supported = not any(
        unit["unsafe"]
        for unit in own["units"] + opponent["units"]
    )

    combat = 0.0
    if not (own["dead"] or opponent["dead"]):
        combat = (
            _best_attack(room, own, opponent, parameters)
            - _best_attack(room, opponent, own, parameters)
        )

    tactical_weight = parameters["board_tactical_weight"]

    advantages = {
        "resource": _advantage(
            own["assets"] - opponent["assets"],
            parameters["resource_scale"],
        ),
        "board": (
            (1.0 - tactical_weight) * material
            + tactical_weight * combat
        ),
        "mana": own["mana"] - opponent["mana"],
        "life": own["life"] - opponent["life"],
    }

    base_score = _weighted_score(advantages, parameters)
    terminal = own["dead"] or opponent["dead"]

    if terminal:
        base_score = (
            float(opponent["dead"]) - float(own["dead"])
        )

    return {
        "reward": base_score,
        "base_score": base_score,
        "terminal": terminal,
        **{
            f"{name}_advantage": value
            for name, value in advantages.items()
        },
        "board_material_advantage": material,
        "board_combat_advantage": combat,
        "board_combat_supported": combat_supported,
        "board_combat_approximate": True,
        "assets_self": own["assets"],
        "assets_oppo": opponent["assets"],
        "mana_capacity_self": own["mana_capacity"],
        "mana_capacity_oppo": opponent["mana_capacity"],
        "score_life_self": own["life"],
        "score_oppo_self": opponent["life"],
        "score_mana": own["mana"],
        "score_hand": len(agent.hand) / 30.0,
        "score_battle_self": own["board"],
        "score_battle_oppo": opponent["board"],
        "score_battle_self_creatures": own["creatures"],
        "score_battle_oppo_creatures": opponent["creatures"],
    }


def _parameters(config: dict) -> dict[str, float]:
    defaults = {
        "resource_weight": 0.30,
        "board_weight": 0.325,
        "mana_weight": 0.10,
        "life_weight": 0.255,
        "resource_scale": 6.0,
        "board_scale": 8.0,
        "mana_scale": 6.0,
        "life_scale": 8.0,
        "power_weight": 0.50,
        "health_weight": 0.25,
        # 场面项：85% 稳态，15% 战术。
        "board_tactical_weight": 0.15,
        # 稳态部分保留一半关键词加成。
        "keyword_prior_scale": 0.50,
        "keyword_bonus_cap": 0.80,
        "unblockable_weight": 0.45,
        "flying_weight": 0.30,
        "menace_weight": 0.15,
        "reach_weight": 0.08,
        "hexproof_weight": 0.25,
        "indestructible_weight": 0.40,
        "lifelink_weight": 0.20,
        "trample_weight": 0.10,
        "vigilance_weight": 0.12,
        "double_strike_weight": 0.25,
        "haste_weight": 0.08,
    }

    parameters = {
        name: float(config.get(name, default))
        for name, default in defaults.items()
    }

    for name, value in parameters.items():
        if (
            not isfinite(value)
            or value < 0
            or (name.endswith("_scale") and value == 0)
        ):
            raise ValueError(
                f"Invalid reward parameter {name}: {value}"
            )

    for name in (
        "board_tactical_weight",
        "keyword_prior_scale",
    ):
        if parameters[name] > 1.0:
            raise ValueError(f"{name} must be in [0, 1]")

    weight_sum = sum(
        parameters[f"{name}_weight"]
        for name in ("resource", "board", "mana", "life")
    )
    if not isfinite(weight_sum) or weight_sum <= 0:
        raise ValueError(
            "Component weights must have a finite positive sum"
        )

    return parameters


def _reserved_cards(room) -> set[int]:
    """排除已经承诺参与当前战斗的生物。"""
    reserved = set()

    if (
        room.get_flag("attacker_defenders")
        and getattr(room, "attacker", None) is not None
    ):
        reserved.add(id(room.attacker))

    for item in room.stack:
        message = (
            (item.get("message") or "")
            .split("||", 1)[0]
            .split("|")
        )
        if len(message) > 1 and message[1] == "select_defender":
            reserved.add(id(item["card"]))

    return reserved


def _unit(room, card, parameters, reserved):
    """读取生物快照，不改变真实游戏状态。"""
    power, health = map(float, card.state)

    flags = {
        name for name in _FLAGS
        if card.get_flag(name)
    }
    buffs = {
        getattr(buff, "card_type", "")
        for buff in getattr(card, "buffs", ())
    }

    attacks = card.get_counter_from_dict("attack_counter")
    ready = (
        id(card) not in reserved
        and "tap" not in flags
        and (
            "summoning_sickness" not in flags
            or "haste" in flags
        )
        and attacks > 0
        and card.player is room.active_player
    )

    bonus = 0.0

    if power > 0:
        # 第一版保守地避免重复计算穿透能力。
        bonus += max(
            parameters["unblockable_weight"]
            if "unblockable" in flags else 0.0,
            parameters["flying_weight"]
            if "flying" in flags else 0.0,
            parameters["menace_weight"]
            if "Menace" in flags else 0.0,
        )

        for flag, name in (
            ("lifelink", "lifelink_weight"),
            ("Trample", "trample_weight"),
            ("Vigilance", "vigilance_weight"),
            ("Double strike", "double_strike_weight"),
        ):
            if flag in flags:
                bonus += parameters[name]

        if (
            ready
            and "haste" in flags
            and "summoning_sickness" in flags
        ):
            bonus += parameters["haste_weight"]

    elif "flying" in flags:
        # 零攻击飞行生物仍有阻挡价值。
        bonus += parameters["reach_weight"]

    if "reach" in flags and "flying" not in flags:
        bonus += parameters["reach_weight"]

    if "Hexproof" in flags:
        bonus += parameters["hexproof_weight"]

    if "Indestructible" in buffs:
        bonus += parameters["indestructible_weight"]

    factor = (
        1.0
        + parameters["keyword_prior_scale"]
        * min(bonus, parameters["keyword_bonus_cap"])
    )

    value = (
        parameters["power_weight"] * max(power, 0.0)
        + parameters["health_weight"] * health
    ) * factor

    # 不把自定义战斗触发当作已经精确模拟。
    unsafe = False
    for name in _COMBAT_HOOKS:
        method = getattr(card, name, None)
        function = getattr(method, "__func__", method)
        module = getattr(function, "__module__", "") or ""

        if module.startswith(("pycards.", "pytreasures.")):
            unsafe = True

    return {
        "card": card,
        "power": max(power, 0.0),
        "health": health,
        "flags": flags,
        "indestructible": "Indestructible" in buffs,
        "ready": ready and power > 0,
        "blocks": (
            id(card) not in reserved
            and "tap" not in flags
        ),
        "factor": factor,
        "value": value,
        "unsafe": unsafe,
    }


def _player_values(room, player, parameters, reserved):
    assets = {id(card) for card in player.hand}
    creature_values = []
    units = []

    for card in player.battlefield:
        active = (
            card.state[1] > 0
            and not card.get_flag("die")
            and not card.get_flag("exile")
        )

        unit = (
            _unit(room, card, parameters, reserved)
            if active else None
        )
        creature_values.append(unit["value"] if unit else 0.0)

        if unit:
            units.append(unit)
            assets.add(id(card))

    mana_capacity = 0.0
    for land in player.land_area:
        if land.get_flag("die") or land.get_flag("exile"):
            continue

        assets.add(id(land))
        mana_capacity += sum(land.generate_mana().values())

    assets.update(
        id(item["card"])
        for item in room.stack
        if item["card"].player is player
    )

    return {
        "assets": len(assets),
        "board": sum(creature_values),
        "creatures": creature_values,
        "units": units,
        "mana_capacity": max(0.0, mana_capacity),
        "mana": _utility(
            mana_capacity, parameters["mana_scale"]
        ),
        "life": _life_utility(
            player.life, parameters["life_scale"]
        ),
        "life_points": float(player.life),
        "life_cap": float(player.ini_life),
        "dead": bool(
            player.life <= 0 or player.get_flag("die")
        ),
    }


def _can_block(room, attacker, defender):
    if (
        not defender["blocks"]
        or "unblockable" in attacker["flags"]
    ):
        return False

    if (
        "flying" in attacker["flags"]
        and not defender["flags"] & {"flying", "reach"}
    ):
        return False

    # 沿用项目当前的地行判定。
    return room.check_landwalk(
        attacker["card"],
        defender["card"].player,
    )


def _after_damage(unit, damage, parameters):
    health = unit["health"] - damage

    if unit["indestructible"] and health <= 0:
        health = min(1.0, unit["health"])

    value = 0.0
    if health > 0:
        value = (
            parameters["power_weight"] * unit["power"]
            + parameters["health_weight"] * health
        ) * unit["factor"]

    return health, value


def _position_score(own, opponent, parameters):
    """战术试算使用基础评分，避免递归计算战术项。"""
    if (
        own["life_points"] <= 0
        or opponent["life_points"] <= 0
    ):
        return (
            float(opponent["life_points"] <= 0)
            - float(own["life_points"] <= 0)
        )

    advantages = {
        "resource": _advantage(
            own["assets"] - opponent["assets"],
            parameters["resource_scale"],
        ),
        "board": _advantage(
            own["board"] - opponent["board"],
            parameters["board_scale"],
        ),
        "mana": own["mana"] - opponent["mana"],
        "life": (
            _life_utility(
                own["life_points"], parameters["life_scale"]
            )
            - _life_utility(
                opponent["life_points"],
                parameters["life_scale"],
            )
        ),
    }
    return _weighted_score(advantages, parameters)


def _attack_score(
    own,
    opponent,
    attacker,
    defender,
    parameters,
):
    """仅修改局部数值字典，不执行游戏动作或技能。"""
    after_own = dict(own)
    after_opponent = dict(opponent)

    face_damage = attacker["power"]
    heal_own = (
        attacker["power"]
        if "lifelink" in attacker["flags"] else 0.0
    )
    heal_opponent = 0.0

    if defender is not None:
        own_health, own_value = _after_damage(
            attacker, defender["power"], parameters
        )
        opponent_health, opponent_value = _after_damage(
            defender, attacker["power"], parameters
        )

        after_own["board"] += (
            own_value - attacker["value"]
        )
        after_opponent["board"] += (
            opponent_value - defender["value"]
        )

        after_own["assets"] -= int(own_health <= 0)
        after_opponent["assets"] -= int(
            opponent_health <= 0
        )

        face_damage = (
            max(0.0, -opponent_health)
            if "Trample" in attacker["flags"] else 0.0
        )

        # 项目当前实现中，践踏伤害也会触发系命。
        if "lifelink" in attacker["flags"]:
            heal_own += face_damage

        if "lifelink" in defender["flags"]:
            heal_opponent = defender["power"]

    # 按当前 Player.gains_life 的 ini_life 上限处理。
    if heal_own:
        after_own["life_points"] = min(
            own["life_cap"],
            own["life_points"] + heal_own,
        )

    if heal_opponent:
        after_opponent["life_points"] = min(
            opponent["life_cap"],
            opponent["life_points"] + heal_opponent,
        )

    after_opponent["life_points"] -= face_damage

    return _position_score(
        after_own, after_opponent, parameters
    )


def _best_attack(room, own, opponent, parameters):
    before = _position_score(own, opponent, parameters)
    best_gain = 0.0  # 允许选择不攻击。

    for attacker in own["units"]:
        if not attacker["ready"] or attacker["unsafe"]:
            continue

        # 防守方可以选择不阻挡。
        worst_outcome = _attack_score(
            own, opponent, attacker, None, parameters
        )

        for defender in opponent["units"]:
            if not _can_block(room, attacker, defender):
                continue

            outcome = _attack_score(
                own, opponent,
                attacker, defender,
                parameters,
            )

            # 未模拟的防守触发采用保守评价。
            if defender["unsafe"]:
                outcome = min(outcome, before)

            worst_outcome = min(worst_outcome, outcome)

        best_gain = max(
            best_gain,
            worst_outcome - before,
        )

    # 基础评分范围为 [-1, 1]，最大改善量为 2。
    return min(1.0, best_gain / 2.0)


def _weighted_score(advantages, parameters):
    weight_sum = sum(
        parameters[f"{name}_weight"]
        for name in advantages
    )
    return sum(
        parameters[f"{name}_weight"] * value
        for name, value in advantages.items()
    ) / weight_sum


def _utility(value, scale):
    return 1.0 - exp(
        -max(0.0, float(value)) / scale
    )


def _advantage(difference, scale):
    return difference / sqrt(
        scale * scale + difference * difference
    )


def _life_utility(life, scale=8.0, reference=20.0):
    life = max(0.0, float(life))

    linear = min(life / reference, 1.0)
    curved = 1.0 - exp(-life / scale)

    return 0.25 * linear + 0.75 * curved