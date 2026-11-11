from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Time_Reversal.model import Time_Reversal


@bind_card(Time_Reversal)
class Time_Reversal_Simulation(Card_Simulation):
    scenario_locks={
        '_stack_scene':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
        "counter.effect": [
            "Cancel the pending effects of all opposing instants and sorceries currently on the stack.",
            "Replace every opposing instant or sorcery effect on the stack with no effect.",
            "All opposing instant and sorcery effects now in the stack are cancelled.",
            "Cancel each currently stacked instant or sorcery controlled by your opponent.",
            "Make the pending effects of your opponent's stacked instants and sorceries do nothing.",
            "Nullify every opposing instant and sorcery effect currently waiting on the stack.",
            "Cancel the effects of all your opponent's instants and sorceries in the current stack.",
            "Every opposing instant or sorcery on the stack has its pending effect replaced with no action.",
            "Turn all current opposing instant and sorcery stack effects into empty effects.",
            "Neutralize each instant or sorcery effect your opponent currently has on the stack.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _stack_scene(self,kind='instant',own_stack=False,lower_count=0):
        self.scenario_prepare()
        self.scenario_stack(kind, own_target=own_stack, lower_count=lower_count)
        for index, item in enumerate(self.room.stack[:-1]):
            if index % 2 == 0:
                old = item["card"]
                owner = old.player.opponent
                zone = "battlefield" if old.type == "Creature" else "graveyard"
                self.unstage_card(old, old.player)
                new = old.copy_for_player(owner)
                self.stage_card(new, owner, zone=zone)
                item["card"] = new
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_instant_own_False_lower_0(self):
        return self._stack_scene('instant',False,0)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_instant_own_False_lower_3(self):
        return self._stack_scene('instant',False,3)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_instant_own_True_lower_0(self):
        return self._stack_scene('instant',True,0)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_instant_own_True_lower_3(self):
        return self._stack_scene('instant',True,3)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_sorcery_own_False_lower_0(self):
        return self._stack_scene('sorcery',False,0)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_sorcery_own_False_lower_3(self):
        return self._stack_scene('sorcery',False,3)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_sorcery_own_True_lower_0(self):
        return self._stack_scene('sorcery',True,0)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_sorcery_own_True_lower_3(self):
        return self._stack_scene('sorcery',True,3)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_creature_own_False_lower_0(self):
        return self._stack_scene('creature',False,0)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_creature_own_False_lower_3(self):
        return self._stack_scene('creature',False,3)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_creature_own_True_lower_0(self):
        return self._stack_scene('creature',True,0)

    @simulate(evidence={'text': ('counter.effect',), 'fields': ('mana_cost',)})
    def simulate_stack_creature_own_True_lower_3(self):
        return self._stack_scene('creature',True,3)

