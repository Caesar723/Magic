from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Warrior_s_Forced_Challenge.model import Warrior_s_Forced_Challenge


@bind_card(Warrior_s_Forced_Challenge)
class Warrior_s_Forced_Challenge_Simulation(Card_Simulation):
    scenario_locks={
        '_fight_scene':('opponent.battlefield', 'self.battlefield'),
    }

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
        "fight.condition": [
            "If the selected opposing creature is different from the countered creature and you still control a creature,",
            "If you have a creature and the opposing target was not the creature just countered,",
            "When the opposing target differs from the countered creature and one of your creatures remains,",
            "If a creature remains under your control and the opposing target is a different creature,",
            "If the selected opposing creature was not countered and you have a creature in play,",
            "When your battlefield has a creature and the opposing target differs from the countered card,",
            "If you still have a creature after countering and selected a different opposing creature,",
            "When the selected opposing creature is not the countered one and you control another creature,",
            "If there is a creature under your control and the opposing target is distinct from the countered card,",
            "If the chosen opposing creature differs from the creature you countered and you retain a creature,",
        ],
        "fight.effect": [
            "have that opposing creature fight a randomly selected creature you control.",
            "make the opposing target fight a random creature on your battlefield.",
            "choose one of your creatures at random and have the opposing target fight it.",
            "have the selected opposing creature fight one of your creatures chosen randomly.",
            "make the target fight a creature chosen at random from those you control.",
            "pick one creature you control at random and have it fight the opposing target.",
            "have the opposing creature fight a randomly chosen creature under your control.",
            "choose a friendly creature at random for the opposing target to fight.",
            "make the targeted opposing creature fight one random creature you control.",
            "have that target fight one creature selected at random from your battlefield.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack("creature")
        return self.scenario_cast(in_stack=True, provide_mana=False)

    def _fight_scene(self, opponent_dies, own_dies, choose_countered=False, own_count=1, own_target=False):
        self.scenario_prepare()
        countered = self.scenario_stack("creature", own_target)
        for _ in range(own_count):
            self.scenario_creature(self.player, power=5 if opponent_dies else 4, health=5, flags={})
        if choose_countered:
            if own_target:
                return self.scenario_skip()
            selected = countered
        else:
            selected = self.scenario_creature(self.player.opponent, power=5 if own_dies else 4, health=5, flags={})
        subaction = 1 + self.player.opponent.battlefield.index(selected)
        return self.scenario_cast((subaction,), in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition', 'fight.effect'), 'fields': ('mana_cost',)})
    def simulate_fight_enemy_survives_self_survives_enemy_spell(self):
        return self._fight_scene(False, False, own_target=False)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition', 'fight.effect'), 'fields': ('mana_cost',)})
    def simulate_fight_enemy_survives_self_survives_self_spell(self):
        return self._fight_scene(False, False, own_target=True)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition', 'fight.effect'), 'fields': ('mana_cost',)})
    def simulate_fight_enemy_survives_self_dies_enemy_spell(self):
        return self._fight_scene(False, True, own_target=False)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition', 'fight.effect'), 'fields': ('mana_cost',)})
    def simulate_fight_enemy_survives_self_dies_self_spell(self):
        return self._fight_scene(False, True, own_target=True)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition', 'fight.effect'), 'fields': ('mana_cost',)})
    def simulate_fight_enemy_dies_self_survives_enemy_spell(self):
        return self._fight_scene(True, False, own_target=False)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition', 'fight.effect'), 'fields': ('mana_cost',)})
    def simulate_fight_enemy_dies_self_survives_self_spell(self):
        return self._fight_scene(True, False, own_target=True)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition', 'fight.effect'), 'fields': ('mana_cost',)})
    def simulate_fight_enemy_dies_self_dies_enemy_spell(self):
        return self._fight_scene(True, True, own_target=False)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition', 'fight.effect'), 'fields': ('mana_cost',)})
    def simulate_fight_enemy_dies_self_dies_self_spell(self):
        return self._fight_scene(True, True, own_target=True)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition'), 'fields': ('mana_cost',)})
    def simulate_choose_countered_creature(self):
        return self._fight_scene(False, False, choose_countered=True)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition'), 'fields': ('mana_cost',)})
    def simulate_no_friendly_creature(self):
        return self._fight_scene(False, False, own_count=0)

    @simulate(evidence={'text': ('counter.effect', 'fight.condition', 'fight.effect'), 'fields': ('mana_cost',)})
    def simulate_multiple_friendly_candidates(self):
        return self._fight_scene(True, False, own_count=3)

