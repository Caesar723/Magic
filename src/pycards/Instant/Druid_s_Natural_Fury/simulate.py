from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Druid_s_Natural_Fury.model import Druid_s_Natural_Fury


@bind_card(Druid_s_Natural_Fury)
class Druid_s_Natural_Fury_Simulation(Card_Simulation):
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
        "token.effect": [
            "Create {token_count} green Beast creature token{token_count_plural}, each with power and toughness equal to that spell's mana value.",
            "Put {token_count} green Beast creature token{token_count_plural} into play, each sized to the countered spell's total mana cost.",
            "Create {token_count_word} green Beast creature token{token_count_plural} with power and toughness equal to the sum of that spell's mana costs.",
            "Summon {token_count} green Beast creature token{token_count_plural}, each with power and toughness matching that spell's mana value.",
            "Create {token_count_word} green Beast creature token{token_count_plural} whose power and toughness each equal the countered spell's total mana value.",
            "Put {token_count} green Beast creature token{token_count_plural} onto the battlefield with power and toughness each equal to that spell's mana value.",
            "Create {token_count} green Beast creature token{token_count_plural}, each with both stats matching the spell's total mana cost.",
            "You create {token_count_word} green Beast creature token{token_count_plural} with power and toughness matching the countered spell's mana value.",
            "Create {token_count} Beast creature token{token_count_plural} that are green and have power and toughness equal to that spell's total mana cost.",
            "Summon {token_count_word} green Beast creature token{token_count_plural}, setting both their power and toughness to the countered spell's mana value.",
        ],
    }

    def _counter_scene(self, target_type="instant", own_target=False, cost=3, lower_count=0):
        self.scenario_prepare()
        self.scenario_stack(target_type, own_target, cost, lower_count=lower_count)
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_stack(self):
        self.scenario_prepare()
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_outside_response(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast()

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_land_on_stack(self):
        self.scenario_prepare()
        self.scenario_stack()
        self.room.env_mana(self.player.opponent, {"W": (1, 1)})
        self.room.stack[-1]["card"] = self.player.opponent.land_area[-1]
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_blocking_creature(self):
        self.scenario_prepare()
        self.scenario_stack("creature")
        self.room.attacker = self.scenario_creature(self.player, flags={})
        self.room.flag_dict["attacker_defenders"] = True
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_0(self):
        return self._counter_scene('instant', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_1(self):
        return self._counter_scene('instant', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_3(self):
        return self._counter_scene('instant', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_6(self):
        return self._counter_scene('instant', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_0(self):
        return self._counter_scene('instant', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_1(self):
        return self._counter_scene('instant', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_3(self):
        return self._counter_scene('instant', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_6(self):
        return self._counter_scene('instant', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_0(self):
        return self._counter_scene('sorcery', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_1(self):
        return self._counter_scene('sorcery', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_3(self):
        return self._counter_scene('sorcery', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_6(self):
        return self._counter_scene('sorcery', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_0(self):
        return self._counter_scene('sorcery', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_1(self):
        return self._counter_scene('sorcery', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_3(self):
        return self._counter_scene('sorcery', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_6(self):
        return self._counter_scene('sorcery', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_0(self):
        return self._counter_scene('creature', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_1(self):
        return self._counter_scene('creature', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_3(self):
        return self._counter_scene('creature', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_6(self):
        return self._counter_scene('creature', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_0(self):
        return self._counter_scene('creature', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_1(self):
        return self._counter_scene('creature', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_3(self):
        return self._counter_scene('creature', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_6(self):
        return self._counter_scene('creature', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_lower_stack_preserved(self):
        return self._counter_scene(lower_count=2)

