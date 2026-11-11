from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Avacyn__Guardian_of_Hope.model import Avacyn__Guardian_of_Hope


@bind_card(Avacyn__Guardian_of_Hope)
class Avacyn__Guardian_of_Hope_Simulation(Card_Simulation):
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
        "keyword.vigilance": [
            "Vigilance.",
            "This creature has vigilance.",
            "{card_name} has vigilance.",
            "This creature has the vigilance ability.",
            "{card_name} has the vigilance ability.",
            "Attacking does not cause this creature to tap.",
            "This creature does not tap when it attacks.",
            "{card_name} does not tap when it attacks.",
            "Vigilance (Attacking does not cause this creature to tap).",
            "This creature has vigilance and does not tap when it attacks.",
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
        "enter.trigger": [
            "When {card_name} enters the battlefield,",
            "Whenever {card_name} enters the battlefield,",
            "When this creature enters the battlefield,",
            "Whenever this creature enters the battlefield,",
            "When {card_name} enters play,",
            "Whenever {card_name} enters play,",
            "When this creature enters play,",
            "Whenever this creature enters play,",
            "When {card_name} comes into play,",
            "Whenever {card_name} comes into play,",
        ],
        "enter.effect": [
            "creatures you control gain indestructible until your turn ends.",
            "all your creatures gain indestructible until your turn ends.",
            "give each creature you control indestructible until your turn ends.",
            "every creature under your control gains indestructible until your turn ends.",
            "until your turn ends, your creatures have indestructible.",
            "grant indestructible to all creatures you control until your turn ends.",
            "each creature on your battlefield gains indestructible until your turn ends.",
            "give your creatures indestructible until your turn ends.",
            "until your turn ends, all creatures you control gain indestructible.",
            "all creatures under your control receive indestructible until your turn ends.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.vigilance', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.vigilance', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.vigilance', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.vigilance', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.vigilance', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.vigilance', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.vigilance', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.vigilance', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
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

    @simulate(evidence={'text': ('keyword.vigilance', 'keyword.lifelink'), 'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'text': ('keyword.vigilance', 'keyword.lifelink'), 'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_block_flying_creature(self):
        return self.scenario_combat(True, False, False, enemy_flags={"flying": True})

    def _enter_scene(self, own_count, enemy_count, power_offset=0, source_power_offset=None):
        self.scenario_prepare()
        threshold = self.card.effect_params.get("power_threshold", 3)
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for _ in range(count):
                self.scenario_creature(owner, power=max(0, threshold + power_offset), health=8, flags={})
        if source_power_offset is not None:
            self.card.power = self.card.actual_power = max(0, threshold + source_power_offset)
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_0_enemy_0_normal(self):
        return self._enter_scene(0, 0, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_1_enemy_0_normal(self):
        return self._enter_scene(1, 0, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_0_enemy_1_normal(self):
        return self._enter_scene(0, 1, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_1_enemy_1_normal(self):
        return self._enter_scene(1, 1, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_3_enemy_3_normal(self):
        return self._enter_scene(3, 3, 0)

