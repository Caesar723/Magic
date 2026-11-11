from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Soul_Devourer.model import Soul_Devourer


@bind_card(Soul_Devourer)
class Soul_Devourer_Simulation(Card_Simulation):
    scenario_locks={
    }

    text_parts = {
        "death.trigger": [
            "Whenever another creature dies while this creature is on your battlefield,",
            "When another creature dies with this creature still on your battlefield,",
            "Each other creature death while this creature is in play triggers this.",
            "Whenever a different creature dies and this creature remains on your battlefield,",
            "When another creature is put into a graveyard by death while this creature is on your side,",
            "For each other creature that dies while this creature is in play,",
            "Whenever this creature is on your battlefield and another creature dies,",
            "When a creature other than this one dies with this creature on your battlefield,",
            "While this creature remains in play, each other creature death triggers this.",
            "Whenever another creature dies and this creature is still on your battlefield,",
        ],
        "death.effect": [
            "it gains a permanent +{power_bonus}/+{toughness_bonus} buff for each positive point of the dead creature's current power.",
            "give it +{power_bonus}/+{toughness_bonus} permanently repeated for the dead creature's current power, doing nothing for non-positive power.",
            "apply a permanent +{power_bonus}/+{toughness_bonus} buff once per positive current power of the creature that died.",
            "it permanently gets +{power_bonus}/+{toughness_bonus} repeated by the dead creature's current power, treating negative power as zero.",
            "grant it permanent +{power_bonus}/+{toughness_bonus} buffs equal in count to the dead creature's positive current power.",
            "it gains one permanent +{power_bonus}/+{toughness_bonus} bonus for every positive point of that creature's current power.",
            "add permanent +{power_bonus}/+{toughness_bonus} buffs to it, one per positive current power of the dead creature.",
            "increase its stats by +{power_bonus}/+{toughness_bonus} once for each positive current power of the creature that died, with no expiry.",
            "its permanent +{power_bonus}/+{toughness_bonus} bonuses number the positive current power of the dead creature.",
            "give it a permanent +{power_bonus}/+{toughness_bonus} bonus for every positive unit of that dead creature's current power.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_when_cast(self):
        self.scenario_prepare()
        return self.scenario_cast()

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.effect')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.effect')})
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.effect')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.effect')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.effect')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.effect')})
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.effect')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.effect')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

