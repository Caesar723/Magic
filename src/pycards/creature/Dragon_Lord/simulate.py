from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Dragon_Lord.model import Dragon_Lord


@bind_card(Dragon_Lord)
class Dragon_Lord_Simulation(Card_Simulation):
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
        "damage.trigger": [
            "Whenever this creature deals damage to an opposing creature or player, even a zero-damage attempt,",
            "After this creature attempts damage on an opposing creature or player, including zero damage,",
            "Each damage attempt by this creature against an opposing creature or player triggers this, even at zero.",
            "When this creature attempts to damage an opposing creature or the opposing player, even for zero,",
            "Whenever damage is attempted by this creature against an opponent's creature or the opponent, including zero,",
            "When this creature deals damage or attempts zero damage to an opposing creature or player,",
            "After each damage attempt on an opposing creature or player by this creature, even if zero,",
            "Whenever this creature damages an opposing creature or player, counting zero-damage attempts,",
            "For each damage attempt by this creature against an opposing creature or player, including zero,",
            "When this creature inflicts or attempts zero damage on an opposing creature or player,",
        ],
        "damage.effect": [
            "create {token_count} {token_power}/{token_toughness} red Dragon tokens.",
            "put {token_count} {token_power}/{token_toughness} red Dragon tokens onto your battlefield.",
            "summon {token_count} red Dragon tokens with stats {token_power}/{token_toughness}.",
            "you create {token_count} {token_power}/{token_toughness} red Dragons.",
            "create a group of {token_count} red Dragon tokens, each {token_power}/{token_toughness}.",
            "add {token_count} red Dragon tokens of size {token_power}/{token_toughness} to your battlefield.",
            "put {token_count} red {token_power}/{token_toughness} Dragon tokens into play.",
            "you summon {token_count} Dragon tokens, each red and {token_power}/{token_toughness}.",
            "create {token_count} red Dragon creature tokens of {token_power}/{token_toughness}.",
            "bring {token_count} {token_power}/{token_toughness} red Dragon tokens onto your battlefield.",
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

    @simulate(evidence={'text': ('keyword.flying', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'damage.effect')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'damage.effect')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'damage.effect')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'damage.effect')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'damage.effect')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'damage.effect')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'damage.effect')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'damage.effect')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('damage.trigger', 'damage.effect')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('damage.trigger', 'damage.effect')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    @simulate(evidence={'text': ('keyword.flying', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_block_flying_creature(self):
        return self.scenario_combat(True, False, False, enemy_flags={"flying": True})

    @simulate(evidence={'text': ('damage.trigger', 'damage.effect'), 'fields': ('attack', 'special_type')})
    def simulate_zero_damage_attempt(self):
        self.card.power = self.card.actual_power = 0
        return self.scenario_unblocked()

