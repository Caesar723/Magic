from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Ravaging_Ghoul.model import Ravaging_Ghoul


@bind_card(Ravaging_Ghoul)
class Ravaging_Ghoul_Simulation(Card_Simulation):
    scenario_locks={
        '_damage_scene':(),
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
        "enter.damage": [
            "it deals {life_loss} damage to your opponent.",
            "{card_name} deals {life_loss} damage to your opponent.",
            "this creature deals {life_loss} damage to your opponent.",
            "it deals {life_loss} damage to the opposing player.",
            "{card_name} deals {life_loss} damage to the opposing player.",
            "this creature deals {life_loss} damage to the opposing player.",
            "it deals {life_loss} points of damage to your opponent.",
            "{card_name} deals {life_loss} points of damage to your opponent.",
            "this creature deals {life_loss} points of damage to your opponent.",
            "it deals an amount of damage equal to {life_loss} to your opponent.",
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

    def _damage_scene(self, offset):
        self.scenario_prepare()
        life = self.card.effect_params["life_loss"] + offset
        if not 1 <= life <= self.player.opponent.ini_life:
            return self.scenario_skip()
        self.player.opponent.life = life
        self.player.life = 1
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.damage'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_below_lethal(self):
        return self._damage_scene(-1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.damage'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_equal_lethal(self):
        return self._damage_scene(0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.damage'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_above_lethal(self):
        return self._damage_scene(1)

