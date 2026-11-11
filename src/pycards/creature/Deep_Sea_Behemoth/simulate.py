from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Deep_Sea_Behemoth.model import Deep_Sea_Behemoth


@bind_card(Deep_Sea_Behemoth)
class Deep_Sea_Behemoth_Simulation(Card_Simulation):
    text_parts = {
        "enter.trigger": [
            "When {card_name} enters the battlefield,",
            "Whenever {card_name} enters the battlefield,",
            "When this creature enters the battlefield,",
            "Whenever this creature enters the battlefield,",
            "When {card_name} enters play,",
            "Whenever {card_name} enters play,",
            "When this creature enters play,",
            "Whenever this creature enters play,",
            "When {card_name} comes into play,",
            "Whenever {card_name} comes into play,",
        ],
        "enter.effect": [
            "Move a target opposing creature under your control. Return it when this creature dies, if it is still on your battlefield.",
            "Take control of a target opposing creature until this creature dies, returning it if it remains on your battlefield.",
            "Put a target opposing creature onto your battlefield under your control. On this creature's death, give it back if still there.",
            "Gain control of the chosen opposing creature. If this creature dies while that target is still on your battlefield, return control.",
            "Take a target creature your opponent controls. Its control returns when this creature dies if the target is still on your field.",
            "Move the selected opposing creature under your control and give it back on this creature's death if it remains on your battlefield.",
            "Control a target opposing creature. When this creature dies, return that target if still on your battlefield.",
            "Steal control of the chosen opposing creature, then return it when this creature dies if it has stayed on your field.",
            "Gain control of one opposing creature you target. It is given back on this creature's death while still on your battlefield.",
            "Take the selected opposing creature under your control, returning it on this creature's death if it is still on your battlefield.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _enter_scene(self, role, offset=1, extra_red=1, option=1, hand_count=1, hexproof=False, power_offset=0, in_stack=False):
        self.scenario_prepare()
        self.player.hand.clear()
        for _ in range(hand_count):
            self.player.append_card(self.card.copy_for_player(self.player), "hand")
        subaction = 0
        if role in ("self_creature", "enemy_creature"):
            owner = self.player if role == "self_creature" else self.player.opponent
            health = self.card.effect_params.get("damage", 2) + offset
            if health <= 0:
                return self.scenario_skip()
            power = max(0, self.card.effect_params.get("power_threshold", 2) + power_offset)
            self.scenario_creature(owner, power=power, health=health, flags={"Hexproof": hexproof})
            subaction = 11 if owner is self.player else 1
        elif role in ("self_player", "enemy_player"):
            owner = self.player if role == "self_player" else self.player.opponent
            life = self.card.effect_params.get("damage", 2) + offset
            if not 1 <= life <= owner.ini_life:
                return self.scenario_skip()
            owner.life = life
            subaction = 22 if owner is self.player else 21
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast((subaction,), provide_mana=False, in_stack=in_stack)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_creature_normal(self):
        return self._enter_scene('self_creature', offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_creature_normal(self):
        return self._enter_scene('enemy_creature', offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_none_normal(self):
        return self._enter_scene('none', offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_creature_hexproof(self):
        return self._enter_scene('self_creature', hexproof=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_creature_hexproof(self):
        return self._enter_scene('enemy_creature', hexproof=True)

