"""V2 material and one-attack estimate with V3 readiness and mana values."""

from math import isfinite

from game.rlearning.rewards.card_game_v2 import _advantage, _best_attack, _can_block, _parameters, _player_values, _reserved_cards, _utility, _weighted_score


class RewardCombat:
    def __init__(self, config=None):
        reward = (config or {}).get("reward", {})
        # Keep V2's tactical estimator and its scoring parameters unchanged.
        self.combat_params = _parameters(reward)
        self.params = dict(self.combat_params)
        defaults = dict(
            resource_weight=0.12, board_weight=0.42, readiness_weight=0.04,
            available_mana_weight=0.10, capacity_weight=0.08, life_weight=0.24,
            available_mana_scale=4.0, capacity_scale=8.0,
        )
        self.params.update({name: float(reward.get(name, value)) for name, value in defaults.items()})
        for name, value in self.params.items():
            if not isfinite(value) or value < 0 or (name.endswith("_scale") and value == 0):
                raise ValueError(f"Invalid reward parameter {name}: {value}")
        self.weight_names = ("resource", "board", "readiness", "available_mana", "capacity", "life")
        weight_sum = sum(self.params[name + "_weight"] for name in self.weight_names)
        if not isfinite(weight_sum) or weight_sum <= 0:
            raise ValueError("Component weights must have a finite positive sum")

    def mana_values(self, player):
        pool = sum(max(0.0, float(value)) for value in player.mana.values())
        capacity, available = 0.0, pool
        for land in player.land_area:
            if land.get_flag("die") or land.get_flag("exile"):
                continue
            production = sum(max(0.0, float(value)) for value in land.generate_mana().values())
            capacity += production
            if land.check_can_use(player)[0]:
                available += production
        return dict(
            available_mana=available, capacity=capacity,
            available_value=_utility(available, self.params["available_mana_scale"]),
            capacity_value=_utility(capacity, self.params["capacity_scale"]),
        )

    def readiness_values(self, room, agent, own, opponent):
        # As in V3: value current attackers and defenders with a legal matchup.
        side = 0 if room.active_player is agent else 1
        values = (own, opponent)
        active, defending = values[side], values[1 - side]
        attackers = [
            unit for unit in active["units"]
            if "tap" not in unit["flags"]
            and unit["card"].get_counter_from_dict("attack_counter") > 0
            and ("summoning_sickness" not in unit["flags"] or "haste" in unit["flags"])
        ]
        usable_defenders = {}
        for attacker in attackers:
            blockers = [
                unit for unit in defending["units"]
                if _can_block(room, attacker, dict(unit, blocks="tap" not in unit["flags"]))
            ]
            if "Menace" in attacker["flags"] and len(blockers) < 2:
                continue
            usable_defenders.update({id(unit["card"]): unit["value"] for unit in blockers})
        ready = [0.0, 0.0]
        ready[side] = sum(unit["value"] for unit in attackers)
        ready[1 - side] = sum(usable_defenders.values())
        return ready

    def reward(self, room, agent):
        p = self.params
        reserved = _reserved_cards(room)
        own = _player_values(room, agent, self.combat_params, reserved)
        opponent = _player_values(room, agent.opponent, self.combat_params, reserved)
        material = _advantage(own["board"] - opponent["board"], p["board_scale"])
        terminal = own["dead"] or opponent["dead"]
        combat = 0.0
        if not terminal:
            combat = (
                _best_attack(room, own, opponent, self.combat_params)
                - _best_attack(room, opponent, own, self.combat_params)
            )

        own_mana = self.mana_values(agent)
        opponent_mana = self.mana_values(agent.opponent)
        # The old V3 built its body factors without reserving pending fighters.
        readiness_own, readiness_opponent = own, opponent
        if reserved:
            readiness_own = _player_values(room, agent, self.combat_params, set())
            readiness_opponent = _player_values(room, agent.opponent, self.combat_params, set())
        readiness = self.readiness_values(room, agent, readiness_own, readiness_opponent)
        tactical_weight = p["board_tactical_weight"]
        advantages = dict(
            resource=_advantage(own["assets"] - opponent["assets"], p["resource_scale"]),
            board=(1.0 - tactical_weight) * material + tactical_weight * combat,
            readiness=_advantage(readiness[0] - readiness[1], p["board_scale"]),
            available_mana=own_mana["available_value"] - opponent_mana["available_value"],
            capacity=own_mana["capacity_value"] - opponent_mana["capacity_value"],
            life=own["life"] - opponent["life"],
        )
        value = _weighted_score(advantages, p)
        if terminal:
            value = float(opponent["dead"]) - float(own["dead"])

        result = {name + "_advantage": part for name, part in advantages.items()}
        result.update(
            reward=value, base_score=value, terminal=terminal,
            mana_advantage=advantages["available_mana"],
            hand_advantage=_advantage(len(agent.hand) - len(agent.opponent.hand), 8.0),
            board_material_advantage=material, board_combat_advantage=combat,
            board_combat_approximate=True,
            board_combat_supported=not any(unit["unsafe"] for unit in own["units"] + opponent["units"]),
            hand_self=len(agent.hand), hand_oppo=len(agent.opponent.hand),
            assets_self=own["assets"], assets_oppo=opponent["assets"],
            mana_available_self=own_mana["available_mana"],
            mana_available_oppo=opponent_mana["available_mana"],
            mana_capacity_self=own_mana["capacity"], mana_capacity_oppo=opponent_mana["capacity"],
            score_life_self=own["life"], score_oppo_self=opponent["life"],
            score_mana=own_mana["available_value"], score_hand=len(agent.hand) / 30.0,
            score_battle_self=own["board"], score_battle_oppo=opponent["board"],
            score_battle_self_creatures=own["creatures"], score_battle_oppo_creatures=opponent["creatures"],
        )
        return result


def get_reward(room, agent, battled_creature=None, attacker=None):
    config = getattr(agent, "config", getattr(room, "config", {}))
    return RewardCombat(config).reward(room, agent)
