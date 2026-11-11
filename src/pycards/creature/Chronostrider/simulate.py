from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Chronostrider.model import Chronostrider


@bind_card(Chronostrider)
class Chronostrider_Simulation(Card_Simulation):
    scenario_locks={
        'simulate_haste_first_turn_attack':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
        "keyword.flash": [
            "Flash.",
            "This creature has flash.",
            "{card_name} has flash.",
            "This creature has the flash ability.",
            "{card_name} has the flash ability.",
            "Flash (You may cast this spell any time you could cast an instant).",
            "You may cast this creature spell any time you could cast an instant.",
            "You may cast {card_name} any time you could cast an instant.",
            "This creature has flash, so you may cast it any time you could cast an instant.",
            "{card_name} has flash, so you may cast it any time you could cast an instant.",
        ],
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
        "enter.effect": [
            "Take {extra_turns} extra turn{extra_turns_plural} after this turn.",
            "After this turn, take {extra_turns} additional turn{extra_turns_plural}.",
            "You get {extra_turns} extra turn{extra_turns_plural} following this one.",
            "Add {extra_turns} extra turn{extra_turns_plural} for yourself after the current turn.",
            "Take {extra_turns_article_an} extra turn{extra_turns_plural} following the current one.",
            "You take {extra_turns} additional turn{extra_turns_plural} after this one ends.",
            "The current turn is followed by {extra_turns} extra turn{extra_turns_plural} for you.",
            "Give yourself {extra_turns} extra turn{extra_turns_plural} after this turn.",
            "You gain {extra_turns} extra turn{extra_turns_plural} to take after this one.",
            "Queue {extra_turns} additional turn{extra_turns_plural} for yourself after the current turn.",
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

    @simulate(evidence={'text': ('keyword.haste',), 'fields': ('attack', 'special_type')})
    def simulate_haste_first_turn_attack(self):
        self.scenario_prepare()
        self.stage_card(self.card)
        self.scenario_fresh_creature(self.card)
        self.room.active_player = self.player
        self.room.non_active_player = self.player.opponent
        self.room.flag_dict["attacker_defenders"] = False
        self.room.simulation_opponent_action = 1
        return {"card": self.card, "type": 1, "action": self.room.sample_action((2, 3))}

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_queued_0(self):
        self.scenario_prepare()
        self.player.counter_dict["extra_turn"] = 0
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_queued_1(self):
        self.scenario_prepare()
        self.player.counter_dict["extra_turn"] = 1
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_queued_3(self):
        self.scenario_prepare()
        self.player.counter_dict["extra_turn"] = 3
        return self.scenario_cast()

    @simulate(evidence={'text': ('keyword.flash', 'enter.trigger', 'enter.effect'), 'fields': ('mana_cost', 'special_type')})
    def simulate_cast_in_response_window(self):
        self.scenario_prepare()
        return self.scenario_cast(in_stack=True)

