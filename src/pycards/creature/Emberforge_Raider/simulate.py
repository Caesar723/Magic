from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Emberforge_Raider.model import Emberforge_Raider


@bind_card(Emberforge_Raider)
class Emberforge_Raider_Simulation(Card_Simulation):
    text_parts = {
        "keyword.haste": [
            "Haste.",
            "This creature has haste.",
            "{card_name} has haste.",
            "This creature has the haste ability.",
            "{card_name} has the haste ability.",
            "Haste (This creature can attack as soon as it comes under your control).",
            "This creature can attack as soon as it comes under your control.",
            "{card_name} can attack as soon as it comes under your control.",
            "This creature has haste and can attack the turn it enters the battlefield.",
            "{card_name} has haste and can attack the turn it enters the battlefield.",
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
        "enter.damage": [
            "it deals {damage} damage to your opponent.",
            "{card_name} deals {damage} damage to your opponent.",
            "this creature deals {damage} damage to your opponent.",
            "it deals {damage} damage to the opposing player.",
            "{card_name} deals {damage} damage to the opposing player.",
            "this creature deals {damage} damage to the opposing player.",
            "it deals {damage} points of damage to your opponent.",
            "{card_name} deals {damage} points of damage to your opponent.",
            "this creature deals {damage} points of damage to your opponent.",
            "it deals an amount of damage equal to {damage} to your opponent.",
        ],
    }

    def _simulate_damage(self, life):
        self.scenario_prepare()
        if not 1 <= life <= self.player.opponent.ini_life:
            return self.scenario_skip()
        self.player.opponent.life = life
        self.player.life = 1
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.damage'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_damage_below_lethal(self):
        return self._simulate_damage(self.card.effect_params["damage"] - 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.damage'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_damage_exact_lethal(self):
        return self._simulate_damage(self.card.effect_params["damage"])

    @simulate(evidence={'text': ('enter.trigger', 'enter.damage'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_damage_survives(self):
        return self._simulate_damage(self.card.effect_params["damage"] + 1)

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

    @simulate(evidence={'text': ('keyword.haste',), 'fields': ('attack', 'special_type')})
    def simulate_haste_first_turn_attack(self):
        self.scenario_prepare()
        self.stage_card(self.card)
        self.card.when_go_to_battlefield(self.player, self.player.opponent)
        self.room.active_player = self.player
        self.room.non_active_player = self.player.opponent
        self.room.flag_dict["attacker_defenders"] = False
        self.room.simulation_opponent_action = 1
        return {"card": self.card, "type": 1, "action": self.room.sample_action((2, 3))}

