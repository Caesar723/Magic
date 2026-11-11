from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Seraph_of_the_Eternal_Flame.model import Seraph_of_the_Eternal_Flame


@bind_card(Seraph_of_the_Eternal_Flame)
class Seraph_of_the_Eternal_Flame_Simulation(Card_Simulation):
    text_parts = {
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
        "attack.effect": [
            "all creatures you currently control gain indestructible until your end step.",
            "give each creature currently on your battlefield indestructible until your turn ends.",
            "grant your current creatures indestructible through your turn.",
            "until your end step, each creature already on your battlefield has indestructible.",
            "your existing battlefield creatures receive indestructible until your turn ends.",
            "apply indestructible to every creature now under your control until your end step.",
            "each of your current creatures is granted indestructible until the end of your turn.",
            "give indestructible to your creatures currently in play until your end step.",
            "your creatures now on the battlefield gain the indestructible ability until your turn ends.",
            "grant indestructible until your end step to all creatures you currently have in play.",
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

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

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _protected_attack(self, friends, enemy_dies, extra_damage):
        self.scenario_prepare()
        for _ in range(friends):
            self.scenario_creature(self.player, power=1, health=3, flags={})
        self.scenario_creature(self.player.opponent, power=self.card.state[1] + extra_damage, health=self.card.state[0] if enemy_dies else self.card.state[0] + 1, flags={})
        record = self.room.simulate_creature_attack(self.card)
        self.stage_card(self.card)
        self.scenario_block()
        return record

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_0_enemy_dies_False_damage_0(self):
        return self._protected_attack(0, False, 0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_0_enemy_dies_False_damage_5(self):
        return self._protected_attack(0, False, 5)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_0_enemy_dies_True_damage_0(self):
        return self._protected_attack(0, True, 0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_0_enemy_dies_True_damage_5(self):
        return self._protected_attack(0, True, 5)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_1_enemy_dies_False_damage_0(self):
        return self._protected_attack(1, False, 0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_1_enemy_dies_False_damage_5(self):
        return self._protected_attack(1, False, 5)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_1_enemy_dies_True_damage_0(self):
        return self._protected_attack(1, True, 0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_1_enemy_dies_True_damage_5(self):
        return self._protected_attack(1, True, 5)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_3_enemy_dies_False_damage_0(self):
        return self._protected_attack(3, False, 0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_3_enemy_dies_False_damage_5(self):
        return self._protected_attack(3, False, 5)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_3_enemy_dies_True_damage_0(self):
        return self._protected_attack(3, True, 0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_protected_friends_3_enemy_dies_True_damage_5(self):
        return self._protected_attack(3, True, 5)

