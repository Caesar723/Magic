from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Celestial_Herald.model import Celestial_Herald


@bind_card(Celestial_Herald)
class Celestial_Herald_Simulation(Card_Simulation):
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
        "keyword.lifelink": [
            "Lifelink.",
            "This creature has lifelink.",
            "{card_name} has lifelink.",
            "This creature has the lifelink ability.",
            "{card_name} has the lifelink ability.",
            "Lifelink (Damage dealt by this creature also causes you to gain that much life).",
            "Damage dealt by this creature also causes you to gain that much life.",
            "Damage dealt by {card_name} also causes you to gain that much life.",
            "This creature has lifelink, so its damage also causes you to gain that much life.",
            "{card_name} has lifelink, so its damage also causes you to gain that much life.",
        ],
        "upkeep.trigger": [
            "At the beginning of your upkeep, if this creature is still on your battlefield,",
            "When your turn begins, provided this creature remains on your battlefield,",
            "At your upkeep, while this creature is in play under your control,",
            "When your upkeep begins and this creature is on your battlefield,",
            "At the start of your turn, if this creature is still in play on your side,",
            "During your upkeep, if this creature remains on your battlefield,",
            "When you begin your turn with this creature on your battlefield,",
            "At each of your upkeeps while this creature is on your side,",
            "As your upkeep begins, if this creature is still on your battlefield,",
            "At your turn start, provided this creature is in play under your control,",
        ],
        "upkeep.effect": [
            "exile a random opposing creature if available, then return a fresh copy of the creature stored by this ability on your previous upkeep, if any.",
            "randomly exile an available opposing creature, then give back a fresh copy of the creature this ability stored last upkeep.",
            "choose an opposing creature randomly to exile if one exists, then return the previously stored creature as a fresh battlefield copy.",
            "exile one random opposing creature when available, then return a fresh copy of the creature kept from the previous upkeep.",
            "randomly put an opposing creature into exile if possible, then return the prior stored creature as a fresh copy.",
            "exile an available opposing creature at random and afterward return a fresh copy of the previously stored creature.",
            "take one random opposing creature into exile if any exist, then bring back the previous upkeep's stored creature as a fresh copy.",
            "randomly exile one available creature your opponent controls, then return a fresh copy of the prior stored creature.",
            "put a random opposing creature into exile when possible, then return the creature stored on the preceding upkeep as a fresh copy.",
            "choose one available opposing creature randomly for exile, then restore a fresh copy of the creature stored last upkeep.",
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

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_block_flying_creature(self):
        return self.scenario_combat(True, False, False, enemy_flags={"flying": True})

