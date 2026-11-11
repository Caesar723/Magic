from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Priest_s_Divine_Binding.model import Priest_s_Divine_Binding


@bind_card(Priest_s_Divine_Binding)
class Priest_s_Divine_Binding_Simulation(Card_Simulation):
    text_parts = {
        "counter.effect": [
            "Counter the creature spell on top of the stack.",
            "Counter the top spell on the stack if it is a creature.",
            "Remove the top creature spell from the stack without resolving it.",
            "Counter the creature spell currently on top of the stack.",
            "Stop the top creature spell on the stack from resolving.",
            "Counter the spell at the top of the stack, restricted to creatures.",
            "Cancel the creature spell at the top of the stack.",
            "Counter the topmost spell on the stack if it is a creature.",
            "Prevent the creature spell on top of the stack from resolving.",
            "Counter the current top spell on the stack, provided it is a creature.",
        ],
        "heal.effect": [
            "You gain life equal to that creature's power.",
            "Gain an amount of life equal to the countered creature's power.",
            "You restore life equal to that creature's power.",
            "Increase your life total by the power of that creature.",
            "Gain life matching the power of the creature you countered.",
            "You gain an amount of life matching that creature's power.",
            "Restore to yourself an amount of life equal to that creature's power.",
            "Gain as much life as the power of that countered creature.",
            "The countered creature's power determines how much life you gain.",
            "You gain life matching the countered creature's power.",
        ],
    }

    def _counter_scene(self, target_type="instant", own_target=False, cost=3, lower_count=0, life_offset=1, power=3):
        self.scenario_prepare()
        target = self.scenario_stack(target_type, own_target, cost, power=power, lower_count=lower_count)
        self.player.life = max(1, min(self.player.ini_life, self.player.ini_life - target.state[0] + life_offset))
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_stack(self):
        self.scenario_prepare()
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_outside_response(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast()

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_land_on_stack(self):
        self.scenario_prepare()
        self.scenario_stack()
        self.room.env_mana(self.player.opponent, {"W": (1, 1)})
        self.room.stack[-1]["card"] = self.player.opponent.land_area[-1]
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_blocking_creature(self):
        self.scenario_prepare()
        self.scenario_stack("creature")
        self.room.attacker = self.scenario_creature(self.player, flags={})
        self.room.flag_dict["attacker_defenders"] = True
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_0(self):
        return self._counter_scene('creature', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_1(self):
        return self._counter_scene('creature', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_3(self):
        return self._counter_scene('creature', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_6(self):
        return self._counter_scene('creature', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_0(self):
        return self._counter_scene('creature', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_1(self):
        return self._counter_scene('creature', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_3(self):
        return self._counter_scene('creature', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_6(self):
        return self._counter_scene('creature', True, 6)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_invalid_instant(self):
        self.scenario_prepare()
        self.scenario_stack('instant')
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_invalid_sorcery(self):
        self.scenario_prepare()
        self.scenario_stack('sorcery')
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_heal_injured(self):
        return self._counter_scene("creature", life_offset=-1)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_heal_exact_heal(self):
        return self._counter_scene("creature", life_offset=0)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_heal_near_full(self):
        return self._counter_scene("creature", life_offset=1)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_heal_full(self):
        return self._counter_scene("creature", life_offset=5)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_power_0(self):
        return self._counter_scene("creature", power=0)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_power_1(self):
        return self._counter_scene("creature", power=1)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_power_5(self):
        return self._counter_scene("creature", power=5)

    @simulate(evidence={'text': ('counter.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_lower_stack_preserved(self):
        return self._counter_scene("creature", lower_count=2)

