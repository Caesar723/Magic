from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Titan_Giant.model import Titan_Giant


@bind_card(Titan_Giant)
class Titan_Giant_Simulation(Card_Simulation):
    scenario_locks={
        '_enter_scene':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
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
            "destroy all creatures with power less than {power_threshold}, including this creature if it qualifies.",
            "destroy every creature whose power is below {power_threshold}, including {card_name} if applicable.",
            "destroy each creature with power strictly less than {power_threshold}, even this creature if it meets that condition.",
            "destroy all creatures whose power is lower than {power_threshold}, including this creature when eligible.",
            "destroy every creature with less than {power_threshold} power, including {card_name} if it qualifies.",
            "destroy all creatures below {power_threshold} power, with no exception for this creature.",
            "destroy any creature whose power is strictly below {power_threshold}, including this one if applicable.",
            "destroy each creature with power under {power_threshold}, including this creature if its power is that low.",
            "destroy every creature whose power is below {power_threshold}, without exempting {card_name}.",
            "destroy all creatures with power lower than {power_threshold}, including this one when it meets the threshold condition.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _enter_scene(self, own_count, enemy_count, power_offset=0, source_power_offset=None):
        self.scenario_prepare()
        threshold = self.card.effect_params.get("power_threshold", 3)
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for _ in range(count):
                self.scenario_creature(owner, power=max(0, threshold + power_offset), health=8, flags={})
        if source_power_offset is not None:
            self.card.power = self.card.actual_power = max(0, threshold + source_power_offset)
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_0_enemy_0_below(self):
        return self._enter_scene(0, 0, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_0_enemy_0_equal(self):
        return self._enter_scene(0, 0, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_0_enemy_0_above(self):
        return self._enter_scene(0, 0, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_1_enemy_0_below(self):
        return self._enter_scene(1, 0, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_1_enemy_0_equal(self):
        return self._enter_scene(1, 0, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_1_enemy_0_above(self):
        return self._enter_scene(1, 0, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_0_enemy_1_below(self):
        return self._enter_scene(0, 1, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_0_enemy_1_equal(self):
        return self._enter_scene(0, 1, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_0_enemy_1_above(self):
        return self._enter_scene(0, 1, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_1_enemy_1_below(self):
        return self._enter_scene(1, 1, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_1_enemy_1_equal(self):
        return self._enter_scene(1, 1, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_1_enemy_1_above(self):
        return self._enter_scene(1, 1, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_3_enemy_3_below(self):
        return self._enter_scene(3, 3, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_3_enemy_3_equal(self):
        return self._enter_scene(3, 3, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_self_3_enemy_3_above(self):
        return self._enter_scene(3, 3, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_source_below(self):
        return self._enter_scene(1, 1, 0, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_source_equal(self):
        return self._enter_scene(1, 1, 0, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'attack')})
    def simulate_enter_source_above(self):
        return self._enter_scene(1, 1, 0, 1)

