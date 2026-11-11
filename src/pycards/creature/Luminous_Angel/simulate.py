from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Luminous_Angel.model import Luminous_Angel


@bind_card(Luminous_Angel)
class Luminous_Angel_Simulation(Card_Simulation):
    scenario_locks={
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
        "upkeep.condition": [
            "if your life is at least {life_threshold},",
            "if you have {life_threshold} or more life,",
            "when your life total is no lower than {life_threshold},",
            "if your life meets or exceeds {life_threshold},",
            "if your life total is {life_threshold} or higher,",
            "when you have at least {life_threshold} life,",
            "if your life is equal to or above {life_threshold},",
            "provided your life is no less than {life_threshold},",
            "if your life total reaches {life_threshold} or more,",
            "when your life is at or above {life_threshold},",
        ],
        "upkeep.effect": [
            "this creature permanently gets +{power_bonus}/+{toughness_bonus}.",
            "give this creature a permanent +{power_bonus}/+{toughness_bonus} buff.",
            "its power permanently increases by {power_bonus} and health by {toughness_bonus}.",
            "this creature gains an extra {power_bonus} power and {toughness_bonus} health permanently.",
            "add {power_bonus} power and {toughness_bonus} health to this creature without turn expiry.",
            "grant this creature +{power_bonus}/+{toughness_bonus} permanently.",
            "it receives a permanent +{power_bonus}/+{toughness_bonus} bonus.",
            "permanently increase this creature's power by {power_bonus} and health by {toughness_bonus}.",
            "this creature gets +{power_bonus}/+{toughness_bonus} with no end-step expiry.",
            "apply a permanent stat bonus of +{power_bonus}/+{toughness_bonus} to this creature.",
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

