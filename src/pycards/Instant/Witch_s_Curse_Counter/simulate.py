from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Witch_s_Curse_Counter.model import Witch_s_Curse_Counter


@bind_card(Witch_s_Curse_Counter)
class Witch_s_Curse_Counter_Simulation(Card_Simulation):
    text_parts = {
        "counter.effect": [
            "Counter the top spell.",
            "Counter the spell on top of the stack.",
            "Remove the stack's top spell without resolving its effect.",
            "Cancel the effect of the topmost spell.",
            "Counter whichever spell is currently on top of the stack.",
            "The top spell on the stack is countered.",
            "Counter the currently topmost spell.",
            "Undo the spell at the top of the stack.",
            "The current top spell is countered.",
            "Cancel the top spell's pending effect.",
        ],
        "target.scope": [
            "Apply this to all creatures your opponent controls.",
            "Affect every creature on your opponent's battlefield.",
            "The following effect applies to all creatures under your opponent's control.",
            "Apply the effect to each creature your opponent controls.",
            "Give every creature on your opponent's side the following effect.",
            "All opposing creatures receive this effect.",
            "Affect each creature under your opponent's control with this effect.",
            "The effect applies to every creature your opponent has in play.",
            "Apply the following effect to all creatures on your opponent's side.",
            "Give this effect to all creatures your opponent controls.",
        ],
        "stats.effect": [
            "Halve its power and remaining health using nearest-even rounding until its controller has ended {duration} turns.",
            "Divide its power and remaining health by two, rounding ties to even, for {duration} of its controller's end steps.",
            "Its power and remaining health are halved with ties rounded to even until {duration} controller end steps pass.",
            "For {duration} end steps of its controller, halve power and remaining health with nearest-even rounding.",
            "Reduce its power and remaining health to half, rounding exact halves to even, until its controller ends {duration} turns.",
            "Use half its power and half its remaining health, rounded to the nearest even integer on ties, for {duration} controller end steps.",
            "The curse halves its power and remaining health with nearest-even rounding and expires after {duration} of its controller's end steps.",
            "Until its controller has reached {duration} end steps, its power and health are halved with ties to even.",
            "Keep its power and remaining health halved using nearest-even rounding through {duration} controller end steps.",
            "Halve both power and remaining health, with half-integer ties rounded to even, until {duration} end steps of its controller occur.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _protection_scene(self, own_count, enemy_count, role="self", selected_index=0, health=3, tapped=False, knight=False, creature_knight=False, library_count=None, time_count=0, stack_type="instant", own_stack=False):
        self.scenario_prepare()
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                creature = self.scenario_creature(owner, power=index + 1, health=health + index, flags={"tap": tapped, "Hexproof": owner is self.player.opponent and index % 2 == 0})
                if knight:
                    creature.type_card = "Human Knight"
                if creature_knight:
                    creature.type_creature = "Knight"
        if library_count is not None:
            self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)})
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        self.scenario_stack(stack_type, own_target=own_stack)
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_1(self):
        return self._protection_scene(0, 0, health=1)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_2(self):
        return self._protection_scene(0, 0, health=2)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_3(self):
        return self._protection_scene(0, 0, health=3)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_5(self):
        return self._protection_scene(0, 0, health=5)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_1(self):
        return self._protection_scene(1, 0, health=1)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_2(self):
        return self._protection_scene(1, 0, health=2)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_3(self):
        return self._protection_scene(1, 0, health=3)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_5(self):
        return self._protection_scene(1, 0, health=5)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_1(self):
        return self._protection_scene(0, 1, health=1)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_2(self):
        return self._protection_scene(0, 1, health=2)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_3(self):
        return self._protection_scene(0, 1, health=3)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_5(self):
        return self._protection_scene(0, 1, health=5)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_1(self):
        return self._protection_scene(1, 1, health=1)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_2(self):
        return self._protection_scene(1, 1, health=2)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_3(self):
        return self._protection_scene(1, 1, health=3)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_5(self):
        return self._protection_scene(1, 1, health=5)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_1(self):
        return self._protection_scene(3, 3, health=1)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_2(self):
        return self._protection_scene(3, 3, health=2)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_3(self):
        return self._protection_scene(3, 3, health=3)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_5(self):
        return self._protection_scene(3, 3, health=5)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_1(self):
        return self._protection_scene(0, 5, health=1)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_2(self):
        return self._protection_scene(0, 5, health=2)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_3(self):
        return self._protection_scene(0, 5, health=3)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_5(self):
        return self._protection_scene(0, 5, health=5)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_already_tapped(self):
        return self._protection_scene(3, 3, tapped=True)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_instant_own_False(self):
        return self._protection_scene(2, 3, stack_type='instant', own_stack=False)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_instant_own_True(self):
        return self._protection_scene(2, 3, stack_type='instant', own_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_sorcery_own_False(self):
        return self._protection_scene(2, 3, stack_type='sorcery', own_stack=False)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_sorcery_own_True(self):
        return self._protection_scene(2, 3, stack_type='sorcery', own_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_creature_own_False(self):
        return self._protection_scene(2, 3, stack_type='creature', own_stack=False)

    @simulate(evidence={'text': ('counter.effect', 'target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_creature_own_True(self):
        return self._protection_scene(2, 3, stack_type='creature', own_stack=True)

