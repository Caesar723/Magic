from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Eternal_Phoenix.model import Eternal_Phoenix


@bind_card(Eternal_Phoenix)
class Eternal_Phoenix_Simulation(Card_Simulation):
    scenario_locks={
        '_marked_combat':(),
    }

    text_parts = {
        "keyword.flying": [
            "Flying.",
            "This creature has flying.",
            "{card_name} has flying.",
            "This creature has the flying ability.",
            "{card_name} has the flying ability.",
            "Flying (Only creatures with flying or reach can block this creature).",
            "This creature can be blocked only by creatures with flying or reach.",
            "Only creatures with flying or reach can block this creature.",
            "Creatures without flying or reach cannot block this creature.",
            "This creature has flying. Creatures without flying or reach cannot block it.",
        ],
        "death.trigger": [
            "When this creature dies,",
            "Whenever this creature dies,",
            "On this creature's death,",
            "When this creature is put into the graveyard by death,",
            "Upon this creature dying,",
            "After this creature dies,",
            "If this creature dies,",
            "When death puts this creature into a graveyard,",
            "As this creature dies,",
            "Whenever this creature is killed,",
        ],
        "death.condition": [
            "if it did not have its feather marker,",
            "if its feather marker was absent,",
            "unless it already had its feather marker,",
            "if it was not marked with a feather,",
            "provided it had no feather marker,",
            "if no feather marker was on it,",
            "when it had not yet gained its feather marker,",
            "if it lacked the feather marker,",
            "as long as it was not already feather-marked,",
            "if its feather marker was not present,",
        ],
        "death.effect": [
            "create a fresh battlefield copy marked with a feather, leaving this original card in the graveyard.",
            "put a fresh feather-marked copy onto your battlefield while the original remains in the graveyard.",
            "return a fresh copy with its feather marker onto your battlefield and retain the original graveyard card.",
            "create a feather-marked battlefield copy without removing the original from your graveyard.",
            "put a new copy onto your battlefield with its feather marker, preserving the original in the graveyard.",
            "summon a fresh copy with a feather marker while this original stays in your graveyard.",
            "make a fresh feather-marked copy on your battlefield, retaining the graveyard original.",
            "return a new feather-marked copy to your battlefield without moving this original out of the graveyard.",
            "create a new battlefield copy carrying a feather marker and leave the original in the graveyard.",
            "put a fresh copy with a feather marker into play, keeping this card in your graveyard.",
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

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'death.trigger', 'death.condition', 'death.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'death.trigger', 'death.condition', 'death.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'death.trigger', 'death.condition', 'death.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'death.trigger', 'death.condition', 'death.effect'), 'fields': ('attack', 'defend', 'special_type')})
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.condition', 'death.effect')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.condition', 'death.effect')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.condition', 'death.effect')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('death.trigger', 'death.condition', 'death.effect')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_block_flying_creature(self):
        return self.scenario_combat(True, False, False, enemy_flags={"flying": True})

    def _marked_combat(self, defending, enemy_dies, self_dies):
        self.card.flag_dict["feather_Eternal_Phoenix"] = True
        return self.scenario_combat(defending, enemy_dies, self_dies)

    @simulate(evidence={'text': ('death.trigger', 'death.condition'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_marked_defending_False_enemy_dies_False(self):
        return self._marked_combat(False, False, True)

    @simulate(evidence={'text': ('death.trigger', 'death.condition'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_marked_defending_False_enemy_dies_True(self):
        return self._marked_combat(False, True, True)

    @simulate(evidence={'text': ('death.trigger', 'death.condition'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_marked_defending_True_enemy_dies_False(self):
        return self._marked_combat(True, False, True)

    @simulate(evidence={'text': ('death.trigger', 'death.condition'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_marked_defending_True_enemy_dies_True(self):
        return self._marked_combat(True, True, True)

