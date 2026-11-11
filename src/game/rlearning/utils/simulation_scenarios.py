import random


class ScenarioTools:
    def description_values(self):
        values = dict(self.card.effect_params, card_name=self.card.name)
        words = (
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
        )
        for name, value in self.card.effect_params.items():
            if type(value) is int:
                word = words[value] if 0 <= value < len(words) else str(value)
                values[name + "_word"] = word
                values[name + "_article"] = "a" if value == 1 else word
                values[name + "_article_an"] = "an" if value == 1 else word
                values[name + "_plural"] = "" if value == 1 else "s"
        return values

    def scenario_prepare(self, parameters=None):
        self.room.clear_environmrnt()
        if parameters is None:
            self.basic_initinal()
        else:
            self.basic_initinal(parameters)
        self.room.env_no_creature(self.player)
        self.room.env_no_creature(self.player.opponent)
        self.random_life()(self.player)
        self.random_life()(self.player.opponent)
        self.room.simulation_opponent_action = None

    def scenario_creature(self, owner, power=None, health=None, flags=None, mana_cost=None, creature_type=None):
        existing = list(owner.battlefield)
        self.room.env_one_creature(owner)
        creature = owner.battlefield[0]
        owner.battlefield = existing
        if power is not None:
            creature.power = creature.actual_power = power
        if health is not None:
            creature.live = creature.actual_live = health
        if flags is not None:
            creature.flag_dict.clear()
            creature.flag_dict.update(flags)
            if "_saved_keywords" in type(creature).__dict__:
                type(creature)._saved_keywords = dict(flags)
            creature.content = ", ".join(name for name, enabled in flags.items() if enabled)
        if mana_cost is not None:
            creature.mana_cost = mana_cost
        if creature_type is not None:
            creature.type_creature = creature.type_card = creature_type
        return self.stage_card(creature, owner)

    def scenario_cast(self, preferred_subactions=(0,), extra_cost=None, in_stack=False, provide_mana=True):
        if provide_mana:
            cost = dict(self.card.calculate_cost())
            for color, amount in (extra_cost or {}).items():
                cost[color] = cost.get(color, 0) + amount
            self.room.env_mana(
                self.player, {color: (0, 0) for color in ("U", "W", "B", "R", "G")}, least_mana=cost
            )
        cast = self.room.simulate_play_in_stack if in_stack else self.room.simulate_play
        return cast(self.card, preferred_subactions=preferred_subactions, populate_targets=False)

    def scenario_skip(self):
        return {"card": self.card, "type": 0, "action": None}

    def scenario_combat(self, defending, opponent_dies, self_dies, margin=0, enemy_flags=None):
        self.scenario_prepare()
        attack, health = self.card.state
        if health <= 0 or (opponent_dies and attack <= margin) or (not self_dies and health <= margin):
            return self.scenario_skip()
        enemy_attack = health + margin if self_dies else health - 1 - margin
        enemy_health = attack - margin if opponent_dies else attack + 1 + margin
        flags = dict(enemy_flags or {})
        if not defending and self.card.get_flag("flying"):
            flags["reach"] = True
        self.scenario_creature(self.player.opponent, enemy_attack, enemy_health, flags)
        if defending:
            result = self.room.simulate_creature_defend(self.card)
        else:
            result = self.room.simulate_creature_attack(self.card)
            self.scenario_block()
        self.stage_card(self.card)
        return result

    def scenario_unblocked(self, with_creature=False):
        self.scenario_prepare()
        if with_creature:
            self.scenario_creature(self.player.opponent, flags={})
        result = self.room.simulate_creature_attack(self.card)
        self.stage_card(self.card)
        self.room.simulation_opponent_action = 1
        return result

    def scenario_stack(self, target_type="instant", own_target=False, cost=2, power=3, lower_count=0):
        target_type = target_type.lower()
        self.room.env_stack_cards(self.player, self.card if target_type == "land" else None, preferred_types=(target_type,))
        top = self.room.stack[-1]
        zones = {"Creature": "battlefield", "Land": "land_area"}
        for item in self.room.stack[:-1]:
            card = item["card"]
            zone = zones.get(card.type, "graveyard")
            card.player.remove_card(card, zone)
        self.room.stack[:] = [top]
        target = top["card"]
        if own_target:
            zone = zones.get(target.type, "graveyard")
            target.player.remove_card(target, zone)
            target = target.copy_for_player(self.player)
            getattr(self.player, zone).append(target)
            top["card"] = target
            top["message"] = random.choice(self.room.all_play_card_messages(self.player))
        target.mana_cost = str(max(0, cost))
        if target.type == "Creature":
            target.power = target.actual_power = power
            target.live = target.actual_live = 4
        for _ in range(lower_count):
            lower = target.copy_for_player(target.player)
            zone = zones.get(lower.type, "graveyard")
            getattr(lower.player, zone).append(lower)
            self.room.stack.insert(0, dict(top, card=lower))
        return target

    def scenario_option(self, option):
        selection_step = self.card.selection_step

        async def choose_option(player=None, opponent=None, selection_random=False):
            send_selection_cards = player.send_selection_cards

            async def select_cards(cards, *args, **kwargs):
                if cards and all(getattr(card, "selection_index", None) in (1, 2) for card in cards):
                    return next(card for card in cards if card.selection_index == option)
                return await send_selection_cards(cards, *args, **kwargs)

            player.send_selection_cards = select_cards
            try:
                return await selection_step(player, opponent, selection_random)
            finally:
                player.send_selection_cards = send_selection_cards

        self.card.selection_step = choose_option

    def scenario_block(self):
        defender = self.player.opponent.battlefield[0]
        if self.card.get_flag("flying") and not (defender.get_flag("flying") or defender.get_flag("reach")):
            defender.flag_dict["reach"] = True
            defender.extra_content.append("Reach.")
            if "_saved_keywords" in type(defender).__dict__:
                type(defender)._saved_keywords["reach"] = True
        self.room.simulation_opponent_action = 12
