from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Mage_s_Veto.model import Mage_s_Veto


@bind_card(Mage_s_Veto)
class Mage_s_Veto_Simulation(Card_Simulation):
    scenario_locks={
        '_counter_scene':('self.library',),
        'simulate_land_on_stack':('opponent.land_area',),
        'simulate_blocking_creature':('self.battlefield',),
    }

    text_parts = {
        "counter.effect": [
            "Counter the nonland spell on top of the stack.",
            "Counter the top spell on the stack if it is not a land.",
            "Remove the top nonland spell from the stack without resolving it.",
            "Counter the nonland spell currently on top of the stack.",
            "Stop the top nonland spell on the stack from resolving.",
            "Counter the spell at the top of the stack, excluding lands.",
            "Cancel the nonland spell at the top of the stack.",
            "Counter the topmost spell on the stack if it is not a land.",
            "Prevent the nonland spell on top of the stack from resolving.",
            "Counter the current top spell on the stack, provided it is not a land.",
        ],
        "tutor.condition": [
            "If the countered spell's mana value is less than {mana_threshold},",
            "If that spell's total mana cost is below {mana_threshold},",
            "When that spell has a mana value strictly below {mana_threshold},",
            "If the sum of the countered spell's mana costs is less than {mana_threshold},",
            "If the countered spell costs less than {mana_threshold} mana in total,",
            "When the spell's total mana value is below {mana_threshold},",
            "If the countered card has a total mana cost under {mana_threshold},",
            "If that spell's mana value is strictly less than {mana_threshold},",
            "When its total mana cost is less than {mana_threshold},",
            "If the countered spell's total cost is below {mana_threshold},",
        ],
        "tutor.effect": [
            "move the first sorcery card in your library to your hand, if any.",
            "put the earliest sorcery in library order into your hand if one exists.",
            "find the first sorcery card in your library and add it to your hand, if available.",
            "add the first sorcery found in your library to your hand if possible.",
            "move the first sorcery in your library into your hand if your library contains one.",
            "put the first sorcery found from the top of your library into your hand, if any.",
            "find the earliest sorcery card in your library and move it to your hand if one is present.",
            "you receive the first sorcery in your library in your hand, if available.",
            "add the earliest sorcery in your current library order to your hand if possible.",
            "take the first sorcery card out of your library and put it into your hand, if there is one.",
        ],
    }

    def _counter_scene(self, target_type="instant", own_target=False, cost=3, lower_count=0, library_count=None):
        library_count=self.scenario_count("library",library_count)
        self.scenario_prepare()
        self.scenario_stack(target_type, own_target, cost, lower_count=lower_count)
        self.scenario_clear(self.player,"library")
        self.scenario_random_cards(self.player,"library",library_count)
        self.player.library = [card for card in self.player.library if card.type == 'Sorcery'][:library_count]
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_stack(self):
        self.scenario_prepare()
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_outside_response(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast()

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_land_on_stack(self):
        self.scenario_prepare()
        self.scenario_stack()
        self.room.env_mana(self.player.opponent, {"W": (1, 1)})
        self.room.stack[-1]["card"] = self.player.opponent.land_area[-1]
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_blocking_creature(self):
        self.scenario_prepare()
        self.scenario_stack("creature")
        self.room.attacker = self.scenario_creature(self.player, flags={})
        self.room.flag_dict["attacker_defenders"] = True
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_0(self):
        return self._counter_scene('instant', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_1(self):
        return self._counter_scene('instant', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_3(self):
        return self._counter_scene('instant', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_6(self):
        return self._counter_scene('instant', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_0(self):
        return self._counter_scene('instant', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_1(self):
        return self._counter_scene('instant', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_3(self):
        return self._counter_scene('instant', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_6(self):
        return self._counter_scene('instant', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_0(self):
        return self._counter_scene('sorcery', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_1(self):
        return self._counter_scene('sorcery', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_3(self):
        return self._counter_scene('sorcery', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_6(self):
        return self._counter_scene('sorcery', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_0(self):
        return self._counter_scene('sorcery', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_1(self):
        return self._counter_scene('sorcery', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_3(self):
        return self._counter_scene('sorcery', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_6(self):
        return self._counter_scene('sorcery', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_0(self):
        return self._counter_scene('creature', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_1(self):
        return self._counter_scene('creature', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_3(self):
        return self._counter_scene('creature', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_6(self):
        return self._counter_scene('creature', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_0(self):
        return self._counter_scene('creature', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_1(self):
        return self._counter_scene('creature', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_3(self):
        return self._counter_scene('creature', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_6(self):
        return self._counter_scene('creature', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_tutor_below_0_sorceries(self):
        return self._counter_scene(cost=max(0, self.card.effect_params["mana_threshold"] + -1), library_count=0)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_tutor_below_1_sorceries(self):
        return self._counter_scene(cost=max(0, self.card.effect_params["mana_threshold"] + -1), library_count=1)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_tutor_below_3_sorceries(self):
        return self._counter_scene(cost=max(0, self.card.effect_params["mana_threshold"] + -1), library_count=3)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_tutor_equal_0_sorceries(self):
        return self._counter_scene(cost=max(0, self.card.effect_params["mana_threshold"] + 0), library_count=0)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_tutor_equal_1_sorceries(self):
        return self._counter_scene(cost=max(0, self.card.effect_params["mana_threshold"] + 0), library_count=1)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_tutor_equal_3_sorceries(self):
        return self._counter_scene(cost=max(0, self.card.effect_params["mana_threshold"] + 0), library_count=3)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_tutor_above_0_sorceries(self):
        return self._counter_scene(cost=max(0, self.card.effect_params["mana_threshold"] + 1), library_count=0)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_tutor_above_1_sorceries(self):
        return self._counter_scene(cost=max(0, self.card.effect_params["mana_threshold"] + 1), library_count=1)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_tutor_above_3_sorceries(self):
        return self._counter_scene(cost=max(0, self.card.effect_params["mana_threshold"] + 1), library_count=3)

    @simulate(evidence={'text': ('counter.effect', 'tutor.condition', 'tutor.effect'), 'fields': ('mana_cost',)})
    def simulate_lower_stack_preserved(self):
        return self._counter_scene(lower_count=2)

