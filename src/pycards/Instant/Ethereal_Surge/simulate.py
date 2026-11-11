from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Ethereal_Surge.model import Ethereal_Surge


@bind_card(Ethereal_Surge)
class Ethereal_Surge_Simulation(Card_Simulation):
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
        "copy.effect": [
            "Remove that card from its owner's graveyard and add a fresh copy to their hand.",
            "Take the countered card out of its owner's graveyard and put a copy into their hand.",
            "Remove the original from its owner's graveyard, then create a copy in their hand.",
            "The countered card is removed from its owner's graveyard, and its owner receives a fresh copy in hand.",
            "Put a copy of the countered card into its owner's hand and remove the original from their graveyard.",
            "Take that card out of its owner's graveyard and give its owner a copy in hand.",
            "Remove the countered card from its owner's graveyard and place a new copy in their hand.",
            "The original card leaves its owner's graveyard, and a copy is added to that player's hand.",
            "Add a fresh copy of that card to its owner's hand, removing the original from their graveyard.",
            "Remove the original card from the graveyard and create a copy in its owner's hand.",
        ],
    }

    def _counter_scene(self, target_type="instant", own_target=False, cost=3, lower_count=0):
        self.scenario_prepare()
        self.scenario_stack(target_type, own_target, cost, lower_count=lower_count)
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_stack(self):
        self.scenario_prepare()
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_outside_response(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast()

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_land_on_stack(self):
        self.scenario_prepare()
        self.scenario_stack()
        self.room.env_mana(self.player.opponent, {"W": (1, 1)})
        self.room.stack[-1]["card"] = self.player.opponent.land_area[-1]
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_blocking_creature(self):
        self.scenario_prepare()
        self.scenario_stack("creature")
        self.room.attacker = self.scenario_creature(self.player, flags={})
        self.room.flag_dict["attacker_defenders"] = True
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_0(self):
        return self._counter_scene('instant', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_1(self):
        return self._counter_scene('instant', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_3(self):
        return self._counter_scene('instant', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_6(self):
        return self._counter_scene('instant', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_0(self):
        return self._counter_scene('instant', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_1(self):
        return self._counter_scene('instant', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_3(self):
        return self._counter_scene('instant', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_6(self):
        return self._counter_scene('instant', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_0(self):
        return self._counter_scene('sorcery', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_1(self):
        return self._counter_scene('sorcery', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_3(self):
        return self._counter_scene('sorcery', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_6(self):
        return self._counter_scene('sorcery', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_0(self):
        return self._counter_scene('sorcery', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_1(self):
        return self._counter_scene('sorcery', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_3(self):
        return self._counter_scene('sorcery', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_6(self):
        return self._counter_scene('sorcery', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_0(self):
        return self._counter_scene('creature', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_1(self):
        return self._counter_scene('creature', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_3(self):
        return self._counter_scene('creature', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_6(self):
        return self._counter_scene('creature', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_0(self):
        return self._counter_scene('creature', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_1(self):
        return self._counter_scene('creature', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_3(self):
        return self._counter_scene('creature', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_6(self):
        return self._counter_scene('creature', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_lower_stack_preserved(self):
        return self._counter_scene(lower_count=2)

