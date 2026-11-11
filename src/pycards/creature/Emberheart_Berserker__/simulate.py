from pycards.land.Mountain.model import Mountain
from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Emberheart_Berserker__.model import Emberheart_Berserker__


@bind_card(Emberheart_Berserker__)
class Emberheart_Berserker___Simulation(Card_Simulation):
    text_parts = {
        "combat.trigger": [
            "Whenever this creature blocks,",
            "When this creature blocks,",
            "Each time this creature blocks,",
            "Whenever this creature starts blocking,",
            "When this creature begins an block,",
            "As this creature blocks,",
            "When an block by this creature begins,",
            "On each block by this creature,",
            "Whenever this creature begins blocking,",
            "At the start of this creature's block,",
        ],
        "combat.effect": [
            "it gets +{power_bonus}/+{toughness_bonus} for each Mountain you control until your end step.",
            "give it a temporary +{power_bonus}/+{toughness_bonus} buff per Mountain you control until your turn ends.",
            "it gains {power_bonus} power and {toughness_bonus} health for each of your Mountains until your end step.",
            "until your end step, apply +{power_bonus}/+{toughness_bonus} to it once per Mountain you control.",
            "it receives +{power_bonus}/+{toughness_bonus} repeated for your number of Mountains until your turn ends.",
            "add {power_bonus} power and {toughness_bonus} health for every Mountain on your side until your end step.",
            "grant it one +{power_bonus}/+{toughness_bonus} bonus per Mountain you control through your turn.",
            "it gets an extra {power_bonus} power and {toughness_bonus} health per Mountain you control until your end step.",
            "each Mountain you control gives it +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "it gains a temporary +{power_bonus}/+{toughness_bonus} bonus for each Mountain you control, expiring at your end step.",
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('combat.trigger', 'combat.effect')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('combat.trigger', 'combat.effect')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('combat.trigger', 'combat.effect')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('combat.trigger', 'combat.effect')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('combat.trigger', 'combat.effect')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('combat.trigger', 'combat.effect')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('combat.trigger', 'combat.effect')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('combat.trigger', 'combat.effect')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _mountain_combat(self, count, defending, enemy_dies, self_dies, margin=0):
        self.scenario_prepare()
        for _ in range(count):
            land = Mountain(self.player)
            land.tap()
            self.stage_card(land, zone="land_area")
        factor = count if defending else 0
        power = self.card.state[0] + factor * self.card.effect_params["power_bonus"]
        health = self.card.state[1] + factor * self.card.effect_params["toughness_bonus"]
        if health <= 0 or (enemy_dies and power <= margin) or (not self_dies and health <= margin):
            return self.scenario_skip()
        enemy_power = health + margin if self_dies else health - 1 - margin
        enemy_health = power - margin if enemy_dies else power + 1 + margin
        self.scenario_creature(self.player.opponent, power=enemy_power, health=enemy_health, flags={})
        record = self.room.simulate_creature_defend(self.card) if defending else self.room.simulate_creature_attack(self.card)
        self.stage_card(self.card)
        if not defending:
            self.scenario_block()
        return record

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_0_defending_False_enemy_dies_False_self_dies_False(self):
        return self._mountain_combat(0, False, False, False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_0_defending_False_enemy_dies_False_self_dies_True(self):
        return self._mountain_combat(0, False, False, True)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_0_defending_False_enemy_dies_True_self_dies_False(self):
        return self._mountain_combat(0, False, True, False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_0_defending_False_enemy_dies_True_self_dies_True(self):
        return self._mountain_combat(0, False, True, True)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_0_defending_True_enemy_dies_False_self_dies_False(self):
        return self._mountain_combat(0, True, False, False)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_0_defending_True_enemy_dies_False_self_dies_True(self):
        return self._mountain_combat(0, True, False, True)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_0_defending_True_enemy_dies_True_self_dies_False(self):
        return self._mountain_combat(0, True, True, False)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_0_defending_True_enemy_dies_True_self_dies_True(self):
        return self._mountain_combat(0, True, True, True)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_1_defending_False_enemy_dies_False_self_dies_False(self):
        return self._mountain_combat(1, False, False, False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_1_defending_False_enemy_dies_False_self_dies_True(self):
        return self._mountain_combat(1, False, False, True)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_1_defending_False_enemy_dies_True_self_dies_False(self):
        return self._mountain_combat(1, False, True, False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_1_defending_False_enemy_dies_True_self_dies_True(self):
        return self._mountain_combat(1, False, True, True)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_1_defending_True_enemy_dies_False_self_dies_False(self):
        return self._mountain_combat(1, True, False, False)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_1_defending_True_enemy_dies_False_self_dies_True(self):
        return self._mountain_combat(1, True, False, True)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_1_defending_True_enemy_dies_True_self_dies_False(self):
        return self._mountain_combat(1, True, True, False)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_1_defending_True_enemy_dies_True_self_dies_True(self):
        return self._mountain_combat(1, True, True, True)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_3_defending_False_enemy_dies_False_self_dies_False(self):
        return self._mountain_combat(3, False, False, False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_3_defending_False_enemy_dies_False_self_dies_True(self):
        return self._mountain_combat(3, False, False, True)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_3_defending_False_enemy_dies_True_self_dies_False(self):
        return self._mountain_combat(3, False, True, False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_3_defending_False_enemy_dies_True_self_dies_True(self):
        return self._mountain_combat(3, False, True, True)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_3_defending_True_enemy_dies_False_self_dies_False(self):
        return self._mountain_combat(3, True, False, False)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_3_defending_True_enemy_dies_False_self_dies_True(self):
        return self._mountain_combat(3, True, False, True)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_3_defending_True_enemy_dies_True_self_dies_False(self):
        return self._mountain_combat(3, True, True, False)

    @simulate(evidence={'text': ('combat.trigger', 'combat.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_mountains_3_defending_True_enemy_dies_True_self_dies_True(self):
        return self._mountain_combat(3, True, True, True)

