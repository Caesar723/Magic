from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Radiant_Angel.model import Radiant_Angel


@bind_card(Radiant_Angel)
class Radiant_Angel_Simulation(Card_Simulation):
    scenario_locks={
        '_color_attack':('opponent.battlefield', 'self.battlefield'),
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
        "damage.trigger": [
            "Whenever this creature deals damage,",
            "Each time this creature deals damage,",
            "When this creature deals any damage,",
            "After this creature deals damage,",
            "Whenever damage is dealt by this creature,",
            "When this creature inflicts damage,",
            "Each damage event caused by this creature triggers this.",
            "When this creature has dealt damage,",
            "After damage is dealt by this creature,",
            "Whenever this creature inflicts damage on anything,",
        ],
        "damage.effect": [
            "tap all creatures whose color label is exactly black on both sides and lock them until their controllers' end steps, then untap them.",
            "all creatures on either side with color exactly black become tapped and cannot untap until their controllers' end steps, then untap.",
            "tap and lock every exactly black-colored creature on both battlefields until its controller's end step, then untap it.",
            "give each creature with color label black a tap lock until its controller's end step, followed by untapping it.",
            "tap all creatures labeled black on either battlefield, prevent their untapping until their controllers' end steps, and untap them then.",
            "every creature whose color is exactly black receives a tap lock until its controller's end step, then untaps.",
            "tap each exactly black-colored creature in play, lock it through its controller's turn, and untap it at that end step.",
            "apply tap locks to all creatures labeled exactly black on both sides until their controllers' end steps, then untap them.",
            "tap and lock the exactly black creatures on both battlefields until each controller's end step, when they untap.",
            "all creatures with color exactly black are tapped, locked until their controllers' end steps, and then untapped.",
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

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'text': ('keyword.lifelink', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    @simulate(evidence={'text': ('keyword.flying', 'damage.trigger', 'damage.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_block_flying_creature(self):
        return self.scenario_combat(True, False, False, enemy_flags={"flying": True})

    def _color_attack(self, own_color, enemy_color):
        record = self.scenario_unblocked(True)
        self.player.opponent.battlefield[0].color = enemy_color
        creature = self.scenario_creature(self.player, power=1, health=3, flags={})
        creature.color = own_color
        return record

    @simulate(evidence={'text': ('damage.trigger', 'damage.effect', 'keyword.lifelink'), 'fields': ('attack', 'special_type')})
    def simulate_color_self_black_enemy_black(self):
        return self._color_attack('black', 'black')

    @simulate(evidence={'text': ('damage.trigger', 'damage.effect', 'keyword.lifelink'), 'fields': ('attack', 'special_type')})
    def simulate_color_self_black_enemy_red(self):
        return self._color_attack('black', 'red')

    @simulate(evidence={'text': ('damage.trigger', 'damage.effect', 'keyword.lifelink'), 'fields': ('attack', 'special_type')})
    def simulate_color_self_black_enemy_gold(self):
        return self._color_attack('black', 'gold')

    @simulate(evidence={'text': ('damage.trigger', 'damage.effect', 'keyword.lifelink'), 'fields': ('attack', 'special_type')})
    def simulate_color_self_blue_enemy_black(self):
        return self._color_attack('blue', 'black')

    @simulate(evidence={'text': ('damage.trigger', 'damage.effect', 'keyword.lifelink'), 'fields': ('attack', 'special_type')})
    def simulate_color_self_blue_enemy_red(self):
        return self._color_attack('blue', 'red')

    @simulate(evidence={'text': ('damage.trigger', 'damage.effect', 'keyword.lifelink'), 'fields': ('attack', 'special_type')})
    def simulate_color_self_blue_enemy_gold(self):
        return self._color_attack('blue', 'gold')

