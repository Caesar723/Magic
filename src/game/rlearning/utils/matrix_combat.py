import numpy as np
from itertools import islice, permutations


class MatrixCombat:
    def __init__(self, config=None):
        config = config or {}
        options = config.get("combat_potential", {})
        self.max_nodes = max(1, int(options.get("max_nodes", 2000)))
        self.max_depth = max(1, int(options.get("max_depth", 8)))
        self.max_orders = max(1, int(options.get("max_orders", 128)))
        self.max_blockers = max(0, int(options.get("max_blockers", 0)))
        self.count_each_fight = options.get("count_each_fight", True)
        self.tap_defender = options.get("tap_defender", True)
        self.trample_extra_lifelink = options.get("trample_extra_lifelink", True)
        self.names = ("flying", "reach", "unblockable", "Menace", "Trample", "lifelink", "Vigilance", "haste", "Double strike", "Indestructible")
        self.flag_ids = {name: index for index, name in enumerate(self.names)}
        defaults = dict(resource_weight=0.30, board_weight=0.325, mana_weight=0.10, life_weight=0.255, resource_scale=6.0, board_scale=8.0, life_scale=8.0, power_weight=0.50, health_weight=0.25)
        reward = config.get("reward", {})
        self.params = {name: float(reward.get(name, value)) for name, value in defaults.items()}

    def empty(self, slots, batch_size=1):
        shape = (batch_size, 2, max(1, slots))
        state = {name: np.zeros(shape, np.float32) for name in ("power", "health")}
        state["factor"] = np.ones(shape, np.float32)
        state.update({name: np.zeros(shape, bool) for name in ("alive", "tapped", "sick")})
        state["attacks"] = np.zeros(shape, np.int32)
        state["flags"] = np.zeros((*shape, len(self.names)), bool)
        state["life"] = np.full((batch_size, 2), 20.0, np.float32)
        state["life_cap"] = state["life"].copy()
        state["dead"] = np.zeros((batch_size, 2), bool)
        state["base_assets"] = np.zeros((batch_size, 2), np.float32)
        state["mana"] = np.zeros((batch_size, 2), np.float32)
        return state

    def take(self, state, indices):
        indices = np.asarray(indices, np.int64)
        return {name: value[indices].copy() for name, value in state.items()}

    def from_room(self, room, agent):
        from game.rlearning.rewards.card_game_v2 import _player_values, _parameters

        players = (agent, agent.opponent)
        state = self.empty(max(len(player.battlefield) for player in players))
        params = _parameters(agent.config.get("reward", {}))
        for side, player in enumerate(players):
            values = _player_values(room, player, params, set())
            units = {id(unit["card"]): unit for unit in values["units"]}
            state["life"][0, side] = player.life
            state["life_cap"][0, side] = player.ini_life
            state["dead"][0, side] = values["dead"]
            state["base_assets"][0, side] = values["assets"] - len(units)
            state["mana"][0, side] = values["mana"]
            for slot, card in enumerate(player.battlefield):
                unit = units.get(id(card))
                if unit is None:
                    continue
                state["power"][0, side, slot] = unit["power"]
                state["health"][0, side, slot] = unit["health"]
                state["factor"][0, side, slot] = unit["factor"]
                state["alive"][0, side, slot] = True
                state["tapped"][0, side, slot] = card.get_flag("tap")
                state["sick"][0, side, slot] = card.get_flag("summoning_sickness")
                state["attacks"][0, side, slot] = max(0, card.get_counter_from_dict("attack_counter"))
                for name, index in self.flag_ids.items():
                    state["flags"][0, side, slot, index] = card.get_flag(name)
                state["flags"][0, side, slot, self.flag_ids["Indestructible"]] = unit["indestructible"]
                if not room.check_landwalk(card, player.opponent):
                    state["flags"][0, side, slot, self.flag_ids["unblockable"]] = True
        return state

    def flag(self, state, side, slots, name):
        rows = np.arange(len(state["life"]))
        return state["flags"][rows, side, slots, self.flag_ids[name]]

    def terminal(self, state):
        return (state["dead"] | (state["life"] <= 0)).any(axis=1)

    def legal_attacks(self, state, side):
        haste = state["flags"][:, side, :, self.flag_ids["haste"]]
        return state["alive"][:, side] & ~state["tapped"][:, side] & (state["attacks"][:, side] > 0) & (~state["sick"][:, side] | haste) & ~self.terminal(state)[:, None]

    def legal_blockers(self, state, side, attackers):
        other = 1 - side
        legal = state["alive"][:, other] & ~state["tapped"][:, other]
        flying = state["flags"][:, other, :, self.flag_ids["flying"]]
        reach = state["flags"][:, other, :, self.flag_ids["reach"]]
        legal &= ~self.flag(state, side, attackers, "flying")[:, None] | flying | reach
        legal &= ~self.flag(state, side, attackers, "unblockable")[:, None]
        return legal & ~self.terminal(state)[:, None]

    def heal(self, state, rows, side, amount):
        positive = amount > 0
        rows, amount = rows[positive], amount[positive]
        state["life"][rows, side] = np.minimum(state["life_cap"][rows, side], state["life"][rows, side] + amount)

    def hurt_player(self, state, rows, side, amount):
        state["life"][rows, side] -= amount
        state["dead"][rows, side] |= state["life"][rows, side] <= 0

    def fight(self, state, side, attackers, blockers, active):
        rows = np.flatnonzero(active)
        if not len(rows):
            return
        other = 1 - side
        a, b = attackers[rows], blockers[rows]
        attack_power = np.maximum(state["power"][rows, side, a], 0)
        block_power = np.maximum(state["power"][rows, other, b], 0)
        attack_health = state["health"][rows, side, a] - block_power
        block_health = state["health"][rows, other, b] - attack_power
        flags = state["flags"]
        attack_health = np.where(flags[rows, side, a, self.flag_ids["Indestructible"]], np.maximum(attack_health, 1), attack_health)
        block_health = np.where(flags[rows, other, b, self.flag_ids["Indestructible"]], np.maximum(block_health, 1), block_health)
        state["health"][rows, side, a] = attack_health
        state["health"][rows, other, b] = block_health
        state["alive"][rows, side, a] = attack_health > 0
        state["alive"][rows, other, b] = block_health > 0
        if self.tap_defender:
            state["tapped"][rows, other, b] = True
        attack_link = flags[rows, side, a, self.flag_ids["lifelink"]]
        block_link = flags[rows, other, b, self.flag_ids["lifelink"]]
        self.heal(state, rows, side, np.where(attack_link, attack_power, 0))
        self.heal(state, rows, other, np.where(block_link, block_power, 0))
        trample = flags[rows, side, a, self.flag_ids["Trample"]]
        overflow = np.where(trample, np.maximum(-block_health, 0), 0)
        self.hurt_player(state, rows, other, overflow)
        if self.trample_extra_lifelink:
            self.heal(state, rows, side, np.where(attack_link, overflow, 0))

    def step(self, state, side, attackers, blocker_orders):
        result = self.take(state, np.arange(len(state["life"])))
        attackers = np.asarray(attackers, np.int64)
        orders = np.asarray(blocker_orders, np.int64)
        batch_size, _, slots = state["power"].shape
        rows = np.arange(batch_size)
        selected = orders >= 0
        safe_a = np.clip(attackers, 0, slots - 1)
        safe_b = np.clip(orders, 0, slots - 1)
        legal = self.legal_blockers(state, side, safe_a)
        valid = (attackers >= 0) & (attackers < slots) & self.legal_attacks(state, side)[rows, safe_a]
        valid &= ((orders == -1) | ((orders >= 0) & (orders < slots))).all(axis=1)
        valid &= (~selected | legal[rows[:, None], safe_b]).all(axis=1)
        counts = np.zeros((batch_size, slots), np.int32)
        rr = np.broadcast_to(rows[:, None], orders.shape)
        np.add.at(counts, (rr[selected], safe_b[selected]), 1)
        valid &= (counts <= 1).all(axis=1)
        sizes = selected.sum(axis=1)
        menace = self.flag(state, side, safe_a, "Menace")
        valid &= (sizes == 0) | ~menace | (sizes >= 2)
        if self.max_blockers:
            valid &= sizes <= self.max_blockers
        no_block = valid & (sizes == 0)
        r = rows[no_block]
        power = np.maximum(result["power"][r, side, safe_a[r]], 0)
        self.hurt_player(result, r, 1 - side, power)
        link = self.flag(result, side, safe_a, "lifelink")[r]
        self.heal(result, r, side, np.where(link, power, 0))
        fights = no_block.astype(np.int32)
        for column in range(orders.shape[1]):
            blockers = safe_b[:, column]
            active = valid & selected[:, column] & ~self.terminal(result)
            active &= result["alive"][rows, side, safe_a] & result["alive"][rows, 1 - side, blockers]
            self.fight(result, side, safe_a, blockers, active)
            fights += active
        r = rows[valid]
        spent = np.maximum(fights[r], 1) if self.count_each_fight else np.ones(len(r), np.int32)
        result["attacks"][r, side, safe_a[r]] = np.maximum(0, result["attacks"][r, side, safe_a[r]] - spent)
        vigilance = self.flag(result, side, safe_a, "Vigilance")
        exhausted = result["attacks"][rows, side, safe_a] <= 0
        result["tapped"][r, side, safe_a[r]] |= exhausted[r] & ~vigilance[r]
        return result, valid

    def score(self, state):
        p = self.params
        values = (p["power_weight"] * np.maximum(state["power"], 0) + p["health_weight"] * np.maximum(state["health"], 0)) * state["factor"]
        board = np.where(state["alive"], values, 0).sum(axis=2)
        assets = state["base_assets"] + state["alive"].sum(axis=2)
        resource_diff = assets[:, 0] - assets[:, 1]
        board_diff = board[:, 0] - board[:, 1]
        life = np.maximum(state["life"], 0)
        utility = 0.25 * np.minimum(life / 20, 1) + 0.75 * (1 - np.exp(-life / p["life_scale"]))
        resource = resource_diff / np.sqrt(p["resource_scale"] ** 2 + resource_diff ** 2)
        material = board_diff / np.sqrt(p["board_scale"] ** 2 + board_diff ** 2)
        mana = state["mana"][:, 0] - state["mana"][:, 1]
        weights = sum(p[name + "_weight"] for name in ("resource", "board", "mana", "life"))
        value = (p["resource_weight"] * resource + p["board_weight"] * material + p["mana_weight"] * mana + p["life_weight"] * (utility[:, 0] - utility[:, 1])) / weights
        dead = state["dead"] | (state["life"] <= 0)
        terminal_value = dead[:, 1].astype(float) - dead[:, 0].astype(float)
        return np.where(dead.any(axis=1), terminal_value, value)

    def block_orders(self, state, side, attacker, selected=()):
        if not selected:
            yield ()
        legal = np.flatnonzero(self.legal_blockers(state, side, np.array([attacker]))[0]).tolist()
        legal = [slot for slot in legal if slot not in selected]
        required = 2 if self.flag(state, side, np.array([attacker]), "Menace")[0] else 1
        minimum = max(0, required - len(selected))
        maximum = min(len(legal), (self.max_blockers or state["power"].shape[2]) - len(selected))
        for count in range(minimum, maximum + 1):
            for extra in permutations(legal, count):
                yield tuple(selected) + extra

    def _defend(self, state, side, attacker, depth, selected=()):
        slots = state["power"].shape[2]
        if attacker < 0 or attacker >= slots or not self.legal_attacks(state, side)[0, attacker]:
            return float(self.score(state)[0]), False, ()
        limit = min(self.max_orders, self.max_nodes - self.nodes)
        if limit <= 0:
            return float(self.score(state)[0]), False, ()
        orders = list(islice(self.block_orders(state, side, attacker, selected), limit + 1))
        if not orders:
            return float(self.score(state)[0]), False, ()
        complete = len(orders) <= limit
        orders = orders[:limit]
        batch = self.take(state, np.zeros(len(orders), np.int64))
        width = max(1, max(map(len, orders)))
        matrix = np.full((len(orders), width), -1, np.int64)
        for index, order in enumerate(orders):
            matrix[index, :len(order)] = order
        children, valid = self.step(batch, side, np.full(len(orders), attacker), matrix)
        self.nodes += len(orders)
        if not valid.any():
            return float(self.score(state)[0]), False, ()
        best = np.inf if side == 0 else -np.inf
        choice = ()
        for index in np.flatnonzero(valid):
            value, exact, _ = self._search(self.take(children, [index]), side, depth + 1)
            complete &= exact
            if (side == 0 and value < best) or (side == 1 and value > best):
                best, choice = value, orders[index]
            if exact and value == (-1 if side == 0 else 1):
                return value, True, orders[index]
        return float(best), complete, choice

    def _search(self, state, side, depth):
        baseline = float(self.score(state)[0])
        attacks = np.flatnonzero(self.legal_attacks(state, side)[0])
        if self.terminal(state)[0] or not len(attacks):
            return baseline, True, None
        if depth >= self.max_depth or self.nodes >= self.max_nodes:
            return baseline, False, None
        key = (depth, side, tuple(value.tobytes() for value in state.values()))
        if key in self.cache:
            return self.cache[key]
        best, complete, choice = baseline, True, None
        for attacker in attacks:
            if self.nodes >= self.max_nodes:
                complete = False
                break
            value, exact, blockers = self._defend(state, side, int(attacker), depth)
            complete &= exact
            if (side == 0 and value > best) or (side == 1 and value < best):
                best, choice = value, (int(attacker), blockers)
            if exact and value == (1 if side == 0 else -1):
                result = value, True, (int(attacker), blockers)
                self.cache[key] = result
                return result
        result = best, complete, choice
        if complete:
            self.cache[key] = result
        return result

    def evaluate(self, state, side):
        self.nodes, self.cache = 0, {}
        baseline = float(self.score(state)[0])
        value, complete, choice = self._search(state, side, 0)
        improvement = value - baseline if side == 0 else baseline - value
        return dict(baseline=baseline, value=value, opportunity=float(np.clip(improvement / 2, 0, 1)), complete=complete, nodes=self.nodes, choice=choice)

    def evaluate_defense(self, state, side, attacker, selected=()):
        self.nodes, self.cache = 0, {}
        value, complete, order = self._defend(state, side, attacker, 0, selected)
        return dict(value=value, complete=complete, nodes=self.nodes, blockers=order)

    def refresh_attackers(self, state, side):
        result = self.take(state, np.arange(len(state["life"])))
        alive = result["alive"][:, side]
        double = result["flags"][:, side, :, self.flag_ids["Double strike"]]
        result["tapped"][:, side] = False
        result["sick"][:, side] = False
        result["attacks"][:, side] = np.where(alive, np.where(double, 2, 1), 0)
        return result