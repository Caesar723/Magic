from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Ephemeral_Response.model import Ephemeral_Response


@bind_card(Ephemeral_Response)
class Ephemeral_Response_Simulation(Card_Simulation):
    text_parts = {
        "counter.condition": [
            "If the top spell belongs to your opponent and their mana pool contains less than {mana_threshold} mana,",
            "If your opponent controls the top spell and has fewer than {mana_threshold} mana in their pool,",
            "When the top spell is your opponent's and their mana pool totals below {mana_threshold},",
            "If the top spell is controlled by the opponent and their mana pool sums to less than {mana_threshold},",
            "If your opponent owns the top spell and their pool holds under {mana_threshold} mana,",
            "When your opponent controls the top spell with a mana pool smaller than {mana_threshold},",
            "If the top spell is your opponent's and they have less than {mana_threshold} pooled mana,",
            "If your opponent has the top spell on the stack and a mana-pool total below {mana_threshold},",
            "When the opponent owns the top spell and has fewer than {mana_threshold} mana in their pool,",
            "If the opposing top spell's controller has less than {mana_threshold} mana in their pool,",
        ],
        "counter.effect": [
            "counter the nonland spell on top of the stack.",
            "counter the top spell on the stack if it is not a land.",
            "remove the top nonland spell from the stack without resolving it.",
            "counter the nonland spell currently on top of the stack.",
            "stop the top nonland spell on the stack from resolving.",
            "counter the spell at the top of the stack, excluding lands.",
            "cancel the nonland spell at the top of the stack.",
            "counter the topmost spell on the stack if it is not a land.",
            "prevent the nonland spell on top of the stack from resolving.",
            "counter the current top spell on the stack, provided it is not a land.",
        ],
        "scry.effect": [
            "look at up to the top {scry_count} cards of your library, keep any of them on top in their existing order, and move the rest to the bottom in their existing order.",
            "examine the top {scry_count} cards of your library or fewer if necessary, keep any on top in order, and put the others on the bottom in order.",
            "inspect up to {scry_count} cards from the top of your library, leaving chosen cards on top and moving the unchosen cards to the bottom without reordering either group.",
            "look at the first {scry_count} available library cards, choose which to keep on top, and put the rest on the bottom while preserving each group's order.",
            "examine up to the first {scry_count} cards of your library, retaining any on top and moving the others to the bottom in their current order.",
            "look through up to the top {scry_count} library cards, leave any chosen cards on top in order, and place the remaining cards at the bottom in order.",
            "inspect the top {scry_count} cards of your library or all of it if smaller, keep any on top, and move the rest to the bottom without changing their relative order.",
            "view up to {scry_count} cards from the top of your library, keep your chosen cards there, and place the rest at the bottom while maintaining both groups' order.",
            "examine at most the top {scry_count} library cards, retaining any chosen cards in place and moving all remaining examined cards to the bottom in order.",
            "look at up to {scry_count} cards from the top, keep any of them there in their current order, and put the remaining examined cards at the bottom in their current order.",
        ],
    }

    def _counter_scene(self, target_type="instant", own_target=False, cost=3, lower_count=0, library_count=5, mana_offset=-1, extra_lands=0):
        self.scenario_prepare()
        self.scenario_stack(target_type, own_target, cost, lower_count=lower_count)
        self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "sorcery_number": (library_count, library_count), "creature_number": (0, 0), "land_number": (0, 0)})
        self.player.library = [card for card in self.player.library if card.type == 'Instant'][:library_count]
        self.player.opponent.mana["colorless"] = max(0, self.card.effect_params["mana_threshold"] + mana_offset)
        if extra_lands:
            self.room.env_mana(self.player.opponent, {"G": (extra_lands, extra_lands)})
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_stack(self):
        self.scenario_prepare()
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_outside_response(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast()

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_land_on_stack(self):
        self.scenario_prepare()
        self.scenario_stack()
        self.room.env_mana(self.player.opponent, {"W": (1, 1)})
        self.room.stack[-1]["card"] = self.player.opponent.land_area[-1]
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_blocking_creature(self):
        self.scenario_prepare()
        self.scenario_stack("creature")
        self.room.attacker = self.scenario_creature(self.player, flags={})
        self.room.flag_dict["attacker_defenders"] = True
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_0(self):
        return self._counter_scene('instant', False, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_1(self):
        return self._counter_scene('instant', False, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_3(self):
        return self._counter_scene('instant', False, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_6(self):
        return self._counter_scene('instant', False, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_0(self):
        return self._counter_scene('instant', True, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_1(self):
        return self._counter_scene('instant', True, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_3(self):
        return self._counter_scene('instant', True, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_6(self):
        return self._counter_scene('instant', True, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_0(self):
        return self._counter_scene('sorcery', False, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_1(self):
        return self._counter_scene('sorcery', False, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_3(self):
        return self._counter_scene('sorcery', False, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_6(self):
        return self._counter_scene('sorcery', False, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_0(self):
        return self._counter_scene('sorcery', True, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_1(self):
        return self._counter_scene('sorcery', True, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_3(self):
        return self._counter_scene('sorcery', True, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_6(self):
        return self._counter_scene('sorcery', True, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_0(self):
        return self._counter_scene('creature', False, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_1(self):
        return self._counter_scene('creature', False, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_3(self):
        return self._counter_scene('creature', False, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_6(self):
        return self._counter_scene('creature', False, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_0(self):
        return self._counter_scene('creature', True, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_1(self):
        return self._counter_scene('creature', True, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_3(self):
        return self._counter_scene('creature', True, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_6(self):
        return self._counter_scene('creature', True, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_mana_below_enemy_spell(self):
        return self._counter_scene(own_target=False, mana_offset=-1)

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_mana_below_self_spell(self):
        return self._counter_scene(own_target=True, mana_offset=-1)

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_mana_equal_enemy_spell(self):
        return self._counter_scene(own_target=False, mana_offset=0)

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_mana_equal_self_spell(self):
        return self._counter_scene(own_target=True, mana_offset=0)

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_mana_above_enemy_spell(self):
        return self._counter_scene(own_target=False, mana_offset=1)

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_mana_above_self_spell(self):
        return self._counter_scene(own_target=True, mana_offset=1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_mana_available_in_lands(self):
        return self._counter_scene(mana_offset=-1, extra_lands=self.card.effect_params["mana_threshold"])

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_lower_stack_preserved(self):
        return self._counter_scene(lower_count=2)

