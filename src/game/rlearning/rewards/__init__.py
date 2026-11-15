import numpy as np
from collections import OrderedDict
from hashlib import blake2b
from itertools import islice
from math import perm
from game.rlearning.utils.matrix_combat import MatrixCombat


class RewardCombat(MatrixCombat):
    def __init__(self, config=None):
        super().__init__(config)
        config = config or {}
        options = config.get("combat_potential", {})
        self.max_nodes = max(1, int(options.get("max_nodes", 128)))
        self.max_depth = max(1, int(options.get("max_depth", 4)))
        self.max_orders = max(1, int(options.get("max_orders", 16)))
        self.seed = int(options.get("seed", 1234))
        self.cache_size = max(0, int(options.get("cache_size", 128)))
        defaults = dict(
            hand_weight=0.12, board_weight=0.34, readiness_weight=0.04,
            available_mana_weight=0.10, capacity_weight=0.08,
            life_weight=0.24, combat_weight=0.08,
            hand_scale=8.0, board_scale=8.0,
            available_mana_scale=4.0, capacity_scale=8.0, life_scale=8.0,
        )
        reward = config.get("reward", {})
        self.params.update({name: float(reward.get(name, value)) for name, value in defaults.items()})
        self.weight_names = ("hand", "board", "readiness", "available_mana", "capacity", "life", "combat")
        self.weight_sum = sum(self.params[name + "_weight"] for name in self.weight_names)
        self.signature = repr((
            self.params, self.max_nodes, self.max_depth, self.max_orders,
            self.max_blockers, self.count_each_fight, self.tap_defender,
            self.trample_extra_lifelink, self.seed,
        ))

    def empty(self, slots, batch_size=1):
        state = super().empty(slots, batch_size)
        state["hand"] = np.zeros((batch_size, 2), np.float32)
        state["available_mana"] = np.zeros((batch_size, 2), np.float32)
        state["capacity"] = np.zeros((batch_size, 2), np.float32)
        state["phase_side"] = np.zeros(batch_size, np.int64)
        return state

    def from_room(self, room, agent):
        state = super().from_room(room, agent)
        state["phase_side"][0] = 0 if room.active_player is agent else 1

        for side, player in enumerate((agent, agent.opponent)):
            state["hand"][0, side] = len(player.hand)
            pool = sum(max(0.0, float(value)) for value in player.mana.values())
            capacity, available = 0.0, pool

            for land in player.land_area:
                if land.get_flag("die") or land.get_flag("exile"):
                    continue
                production = sum(max(0.0, float(value)) for value in land.generate_mana().values())
                capacity += production
                if land.check_can_use(player)[0]:
                    available += production

            state["capacity"][0, side] = capacity
            state["available_mana"][0, side] = available

        return state

    def advantage(self, difference, scale):
        return difference / np.sqrt(scale * scale + difference * difference)

    def life_value(self, life):
        life = np.maximum(life, 0)
        return 0.25 * np.minimum(life / 20.0, 1.0) + 0.75 * (1.0 - np.exp(-life / self.params["life_scale"]))

    def body_values(self, state):
        p = self.params
        alive = state["alive"]
        attack = alive & ~state["tapped"] & (state["attacks"] > 0)
        attack &= ~state["sick"] | state["flags"][:, :, :, self.flag_ids["haste"]]

        rows = np.arange(len(state["life"]))
        side = state["phase_side"]
        other = 1 - side
        active = attack[rows, side]
        defenders = alive[rows, other] & ~state["tapped"][rows, other]

        flying = state["flags"][rows, side, :, self.flag_ids["flying"]]
        unblockable = state["flags"][rows, side, :, self.flag_ids["unblockable"]]
        reach = state["flags"][rows, other, :, self.flag_ids["flying"]]
        reach = reach | state["flags"][rows, other, :, self.flag_ids["reach"]]

        legal = active[:, :, None] & ~unblockable[:, :, None] & defenders[:, None, :]
        legal &= ~flying[:, :, None] | reach[:, None, :]
        menace = state["flags"][rows, side, :, self.flag_ids["Menace"]]
        legal &= (~menace | (legal.sum(axis=2) >= 2))[:, :, None]

        usable = np.zeros_like(alive)
        usable[rows, side] = active
        usable[rows, other] = legal.any(axis=1)

        power = np.maximum(state["power"], 0)
        health = np.maximum(state["health"], 0)
        current = (p["power_weight"] * power + p["health_weight"] * health) * state["factor"]
        body = np.where(alive, current, 0)
        ready = np.where(alive & usable, current, 0)
        return body, ready

    def parts(self, state):
        p = self.params
        body, ready = self.body_values(state)
        board = body.sum(axis=2)
        readiness = ready.sum(axis=2)
        mana = 1.0 - np.exp(-np.maximum(state["available_mana"], 0) / p["available_mana_scale"])
        capacity = 1.0 - np.exp(-np.maximum(state["capacity"], 0) / p["capacity_scale"])
        life = self.life_value(state["life"])
        return dict(
            hand=self.advantage(state["hand"][:, 0] - state["hand"][:, 1], p["hand_scale"]),
            board=self.advantage(board[:, 0] - board[:, 1], p["board_scale"]),
            readiness=self.advantage(readiness[:, 0] - readiness[:, 1], p["board_scale"]),
            available_mana=mana[:, 0] - mana[:, 1],
            capacity=capacity[:, 0] - capacity[:, 1],
            life=life[:, 0] - life[:, 1],
        )

    def score(self, state):
        parts = self.parts(state)
        value = sum(self.params[name + "_weight"] * part for name, part in parts.items()) / self.weight_sum
        dead = state["dead"] | (state["life"] <= 0)
        terminal = dead[:, 1].astype(float) - dead[:, 0].astype(float)
        return np.where(dead.any(axis=1), terminal, value)

    def finish_phase(self, state):
        result = self.take(state, np.arange(len(state["life"])))
        rows = np.arange(len(result["life"]))
        result["attacks"][rows, result["phase_side"]] = 0
        return result

    def state_key(self, state, extra=()):
        digest = blake2b(digest_size=16)
        digest.update(repr((state["power"].shape, extra)).encode())
        for name, value in state.items():
            digest.update(name.encode())
            digest.update(value.tobytes())
        return digest.digest()

    def sample_orders(self, state, side, attacker, selected, limit):
        legal = np.flatnonzero(self.legal_blockers(state, side, np.array([attacker]))[0]).tolist()
        legal = [slot for slot in legal if slot not in selected]
        required = 2 if self.flag(state, side, np.array([attacker]), "Menace")[0] else 1
        minimum = max(0, required - len(selected))
        maximum = min(len(legal), (self.max_blockers or state["power"].shape[2]) - len(selected))
        total = int(not selected) + sum(perm(len(legal), count) for count in range(minimum, maximum + 1))

        if total <= limit:
            return list(self.block_orders(state, side, attacker, selected)), True

        order = [side, 1 - side]
        canonical = {
            name: value[:, order] if value.ndim > 1 and value.shape[1] == 2 else value
            for name, value in state.items()
        }
        canonical["phase_side"] = np.zeros_like(state["phase_side"])
        seed = self.state_key(canonical, (self.seed, attacker, tuple(selected)))
        rng = np.random.default_rng(int.from_bytes(seed[:8], "little"))
        orders, seen = [], set()

        def add(order):
            order = tuple(order)
            if order not in seen and len(orders) < limit:
                seen.add(order)
                orders.append(order)

        if not selected:
            add(())
        elif minimum == 0:
            add(selected)

        if minimum <= 1 <= maximum:
            for slot in rng.permutation(legal):
                add(tuple(selected) + (int(slot),))
        elif minimum == 2 and maximum >= 2:
            shuffled = rng.permutation(legal).tolist()
            for index, slot in enumerate(shuffled):
                add(tuple(selected) + (slot, shuffled[(index + 1) % len(shuffled)]))

        if maximum >= minimum:
            for _ in range(limit * 20):
                count = int(rng.integers(minimum, maximum + 1))
                add(tuple(selected) + tuple(int(slot) for slot in rng.choice(legal, count, replace=False)))
                if len(orders) >= limit:
                    break

        return orders, False

    def _defend(self, state, side, attacker, depth, selected=()):
        slots = state["power"].shape[2]
        if attacker < 0 or attacker >= slots or not self.legal_attacks(state, side)[0, attacker]:
            return float(self.score(state)[0]), False, ()

        limit = min(self.max_orders, self.max_nodes - self.nodes)
        if limit <= 0:
            return float(self.score(state)[0]), False, ()

        orders, complete = self.sample_orders(state, side, attacker, selected, limit)
        if not orders:
            return float(self.score(state)[0]), False, ()

        batch = self.take(state, np.zeros(len(orders), np.int64))
        matrix = np.full((len(orders), max(1, max(map(len, orders)))), -1, np.int64)
        for index, order in enumerate(orders):
            matrix[index, :len(order)] = order

        children, valid = self.step(batch, side, np.full(len(orders), attacker), matrix)
        self.nodes += len(orders)
        if not valid.any():
            return float(self.score(state)[0]), False, ()

        values = self.score(self.finish_phase(children))
        finished = self.terminal(children) | ~self.legal_attacks(children, side).any(axis=1)
        best, choice = (np.inf if side == 0 else -np.inf), ()

        for index in np.flatnonzero(valid):
            if finished[index]:
                value, exact = float(values[index]), True
            elif depth + 1 >= self.max_depth or self.nodes >= self.max_nodes:
                value, exact = float(values[index]), False
            else:
                value, exact, _ = self._search(self.take(children, [index]), side, depth + 1)

            complete &= exact
            if (side == 0 and value < best) or (side == 1 and value > best):
                best, choice = value, orders[index]
            if exact and value == (-1 if side == 0 else 1):
                return value, True, orders[index]

        return float(best), complete, choice

    def _search(self, state, side, depth):
        baseline = float(self.score(self.finish_phase(state))[0])
        attacks = np.flatnonzero(self.legal_attacks(state, side)[0])
        if self.terminal(state)[0] or not len(attacks):
            return baseline, True, None
        if depth >= self.max_depth or self.nodes >= self.max_nodes:
            return baseline, False, None

        key = (depth, side, self.state_key(state))
        if key in self.cache:
            return self.cache[key]

        powers = state["power"][0, side, attacks]
        attacks = attacks[np.argsort(-powers, kind="stable")]
        best, complete, choice = baseline, True, None

        for index, attacker in enumerate(attacks):
            remaining = self.max_nodes - self.nodes
            if remaining <= 0:
                complete = False
                break

            limit = self.max_nodes
            self.max_nodes = self.nodes + max(1, remaining // (len(attacks) - index))
            try:
                value, exact, blockers = self._defend(state, side, int(attacker), depth)
            finally:
                self.max_nodes = limit

            complete &= exact
            if (side == 0 and value > best) or (side == 1 and value < best):
                best, choice = value, (int(attacker), blockers)
            if exact and value == (1 if side == 0 else -1):
                return value, True, (int(attacker), blockers)

        result = best, complete, choice
        if complete:
            self.cache[key] = result
        return result

    def evaluate(self, state, side):
        self.nodes, self.cache = 0, {}
        baseline = float(self.score(self.finish_phase(state))[0])
        value, complete, choice = self._search(state, side, 0)
        improvement = value - baseline if side == 0 else baseline - value
        return dict(
            baseline=baseline, value=value,
            opportunity=float(np.clip(improvement / 2, 0, 1)),
            complete=complete, nodes=self.nodes, choice=choice,
        )

    def combat_value(self, room, agent, state):
        if self.terminal(state)[0]:
            return 0.0, True, 0, False, True

        side = int(state["phase_side"][0])
        player = agent if side == 0 else agent.opponent
        defender = player.opponent
        attacker = getattr(room, "attacker", None)
        pending = bool(room.get_flag("attacker_defenders") and attacker in player.battlefield)
        selected, spells = [], False

        for item in reversed(room.stack):
            message = (item.get("message") or "").split("||", 1)[0].split("|")
            is_block = len(message) > 1 and message[1] == "select_defender"
            if is_block and item["card"] in defender.battlefield:
                selected.append(defender.battlefield.index(item["card"]))
            else:
                spells = True

        if spells:
            return 0.0, False, 0, False, False

        attacker_slot = player.battlefield.index(attacker) if pending else -1
        key = (self.signature, self.state_key(state, (side, attacker_slot, tuple(selected))))
        cache = room.__dict__.setdefault("_reward_v3_combat_cache", OrderedDict())

        if self.cache_size and key in cache:
            value, complete, nodes = cache.pop(key)
            cache[key] = (value, complete, nodes)
            return value, complete, 0, True, True

        if pending:
            result = self.evaluate_defense(state, side, attacker_slot, selected)
        else:
            result = self.evaluate(state, side)

        baseline = float(self.score(self.finish_phase(state))[0])
        value = float(np.clip((result["value"] - baseline) / 2.0, -1.0, 1.0))
        data = value, bool(result["complete"]), int(result["nodes"])

        if self.cache_size:
            cache[key] = data
            while len(cache) > self.cache_size:
                cache.popitem(last=False)

        return (*data, False, True)

    def reward(self, room, agent):
        state = self.from_room(room, agent)
        parts = self.parts(state)
        baseline = float(self.score(state)[0])
        combat, complete, nodes, hit, supported = self.combat_value(room, agent, state)
        terminal = bool(self.terminal(state)[0])
        value = baseline if terminal else baseline + self.params["combat_weight"] * combat / self.weight_sum

        body, _ = self.body_values(state)
        life = self.life_value(state["life"])[0]
        assets = state["base_assets"][0] + state["alive"][0].sum(axis=1)
        result = {name + "_advantage": float(part[0]) for name, part in parts.items()}
        result.update(
            reward=float(value), base_score=float(value), terminal=terminal,
            resource_advantage=result["hand_advantage"], mana_advantage=result["available_mana_advantage"],
            board_material_advantage=result["board_advantage"], board_combat_advantage=combat,
            board_combat_approximate=True, board_combat_supported=supported,
            combat_complete=complete, combat_nodes=nodes, combat_cache_hit=hit,
            hand_self=int(state["hand"][0, 0]), hand_oppo=int(state["hand"][0, 1]),
            assets_self=int(assets[0]), assets_oppo=int(assets[1]),
            mana_available_self=float(state["available_mana"][0, 0]), mana_available_oppo=float(state["available_mana"][0, 1]),
            mana_capacity_self=float(state["capacity"][0, 0]), mana_capacity_oppo=float(state["capacity"][0, 1]),
            score_life_self=float(life[0]), score_oppo_self=float(life[1]),
            score_mana=float(1.0 - np.exp(-state["available_mana"][0, 0] / self.params["available_mana_scale"])),
            score_hand=float(state["hand"][0, 0] / 30.0),
            score_battle_self=float(body[0, 0].sum()), score_battle_oppo=float(body[0, 1].sum()),
            score_battle_self_creatures=body[0, 0].tolist(), score_battle_oppo_creatures=body[0, 1].tolist(),
        )
        return result


def get_reward(room, agent, battled_creature=None, attacker=None):
    config = getattr(agent, "config", getattr(room, "config", {}))
    return RewardCombat(config).reward(room, agent)