from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Thunderclap_Behemoth.model import Thunderclap_Behemoth


@bind_card(Thunderclap_Behemoth)
class Thunderclap_Behemoth_Simulation(Card_Simulation):
    text_parts = {
        "keyword.trample": [
            "Trample.",
            "This creature has trample.",
            "{card_name} has trample.",
            "This creature has the trample ability.",
            "{card_name} has the trample ability.",
            "Trample (This creature can deal excess combat damage to the defending player).",
            "This creature has trample and can deal excess combat damage to the defending player.",
            "{card_name} has trample and can deal excess combat damage to the defending player.",
            "This creature can deal excess combat damage to the defending player through trample.",
            "{card_name} can deal excess combat damage to the defending player through trample.",
        ],
        "attack.trigger": [
            "Whenever this creature attacks,",
            "When this creature attacks,",
            "Each time this creature attacks,",
            "Whenever this creature starts attacking,",
            "When this creature begins an attack,",
            "As this creature attacks,",
            "When an attack by this creature begins,",
            "On each attack by this creature,",
            "Whenever this creature begins attacking,",
            "At the start of this creature's attack,",
        ],
        "attack.condition": [
            "if another creature you control has current power at least {power_threshold},",
            "if a different friendly creature has current power {power_threshold} or greater,",
            "when another creature on your battlefield has current power no lower than {power_threshold},",
            "if any other creature you control has current power at or above {power_threshold},",
            "provided another friendly creature's current power meets or exceeds {power_threshold},",
            "if a creature other than this one on your side has at least {power_threshold} current power,",
            "when a different creature you control reaches {power_threshold} or more current power,",
            "if one of your other creatures has current power equal to or above {power_threshold},",
            "when another friendly creature has at least {power_threshold} power currently,",
            "if another creature under your control has current power no less than {power_threshold},",
        ],
        "attack.effect": [
            "deal {damage} damage to the current defender, whether a creature or player.",
            "hit the creature or player currently defending for {damage} damage.",
            "deal the current defending creature or player {damage} damage.",
            "inflict {damage} damage on this attack's current defender.",
            "the current defender takes {damage} damage, whether creature or player.",
            "deal {damage} damage to the creature or player receiving this attack.",
            "hit this attack's defending creature or player for {damage} damage.",
            "apply {damage} damage to the current defender of this attack.",
            "the creature or player currently defending is dealt {damage} damage.",
            "deal an amount of damage equal to {damage} to this attack's current defender.",
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

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
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

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _condition_combat(self, ally, power_offset=0, health_offset=0, self_dies=False, defending=False, unblocked=False):
        self.scenario_prepare()
        active = ally and power_offset >= 0 and not defending
        if ally:
            self.scenario_creature(self.player, power=max(0, self.card.effect_params["power_threshold"] + power_offset), health=3, flags={})
        health = self.card.state[0] + (self.card.effect_params["damage"] if active else 0) + health_offset
        if health <= 0:
            return self.scenario_skip()
        self.scenario_creature(self.player.opponent, power=self.card.state[1] if self_dies else self.card.state[1] - 1, health=health, flags={})
        record = self.room.simulate_creature_defend(self.card) if defending else self.room.simulate_creature_attack(self.card)
        self.stage_card(self.card)
        if not defending:
            self.room.simulation_opponent_action = 1
            if not unblocked:
                self.scenario_block()
        return record

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_False_power_equal_health_low_self_dies_False(self):
        return self._condition_combat(False, 0, -1, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_False_power_equal_health_low_self_dies_True(self):
        return self._condition_combat(False, 0, -1, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_False_power_equal_health_equal_self_dies_False(self):
        return self._condition_combat(False, 0, 0, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_False_power_equal_health_equal_self_dies_True(self):
        return self._condition_combat(False, 0, 0, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_False_power_equal_health_high_self_dies_False(self):
        return self._condition_combat(False, 0, 1, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_False_power_equal_health_high_self_dies_True(self):
        return self._condition_combat(False, 0, 1, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_below_health_low_self_dies_False(self):
        return self._condition_combat(True, -1, -1, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_below_health_low_self_dies_True(self):
        return self._condition_combat(True, -1, -1, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_below_health_equal_self_dies_False(self):
        return self._condition_combat(True, -1, 0, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_below_health_equal_self_dies_True(self):
        return self._condition_combat(True, -1, 0, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_below_health_high_self_dies_False(self):
        return self._condition_combat(True, -1, 1, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_below_health_high_self_dies_True(self):
        return self._condition_combat(True, -1, 1, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_equal_health_low_self_dies_False(self):
        return self._condition_combat(True, 0, -1, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_equal_health_low_self_dies_True(self):
        return self._condition_combat(True, 0, -1, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_equal_health_equal_self_dies_False(self):
        return self._condition_combat(True, 0, 0, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_equal_health_equal_self_dies_True(self):
        return self._condition_combat(True, 0, 0, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_equal_health_high_self_dies_False(self):
        return self._condition_combat(True, 0, 1, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_equal_health_high_self_dies_True(self):
        return self._condition_combat(True, 0, 1, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_above_health_low_self_dies_False(self):
        return self._condition_combat(True, 1, -1, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_above_health_low_self_dies_True(self):
        return self._condition_combat(True, 1, -1, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_above_health_equal_self_dies_False(self):
        return self._condition_combat(True, 1, 0, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_above_health_equal_self_dies_True(self):
        return self._condition_combat(True, 1, 0, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_above_health_high_self_dies_False(self):
        return self._condition_combat(True, 1, 1, False)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_condition_ally_True_power_above_health_high_self_dies_True(self):
        return self._condition_combat(True, 1, 1, True)

    @simulate(evidence={'text': ('keyword.trample', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_ability_immediate_lethal(self):
        return self._condition_combat(True, health_offset=-self.card.state[0])

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_high_ally_while_defending(self):
        return self._condition_combat(True, defending=True)

    @simulate(evidence={'text': ('attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'special_type')})
    def simulate_ability_hits_player(self):
        return self._condition_combat(True, unblocked=True)

