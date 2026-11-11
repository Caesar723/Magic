from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Harbinger_of_the_Eternal_Tides.model import Harbinger_of_the_Eternal_Tides


@bind_card(Harbinger_of_the_Eternal_Tides)
class Harbinger_of_the_Eternal_Tides_Simulation(Card_Simulation):
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
        "enter.target": [
            "Tap a target creature and prevent it from untapping until its controller's turn ends, then untap it. Choose only a creature your opponent controls.",
            "The target becomes tapped and cannot untap until its controller's end step, when it untaps. Choose only a creature your opponent controls.",
            "Tap the chosen creature, lock it until its controller's turn ends, and untap it at that end step. Choose only a creature your opponent controls.",
            "Make a target creature tapped and unable to untap before its controller's end step, then untap it. Choose only a creature your opponent controls.",
            "Tap the target and block untapping until the end of its controller's turn, then untap it. Choose only a creature your opponent controls.",
            "A target creature becomes tapped, stays locked until its controller's end step, and untaps there. Choose only a creature your opponent controls.",
            "Tap one chosen creature and keep it from untapping until its controller's end step, then untap it. Choose only a creature your opponent controls.",
            "The selected creature is tapped and cannot untap until its controller's turn ends, at which point it untaps. Choose only a creature your opponent controls.",
            "Tap a creature of your choice, prevent its untapping before its controller's end step, and untap it then. Choose only a creature your opponent controls.",
            "Tap the creature you target and stop it untapping until its controller's turn ends, then make it untapped. Choose only a creature your opponent controls.",
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

    def _enter_target(self, role, tapped=False, hexproof=False, in_stack=False):
        self.scenario_prepare()
        subaction = 0
        if role != "none":
            owner = self.player if role == "self" else self.player.opponent
            self.scenario_creature(owner, power=2, health=4, flags={"tap": tapped, "Hexproof": hexproof})
            subaction = 11 if role == "self" else 1
        return self.scenario_cast((subaction,), in_stack=in_stack)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target'), 'fields': ('mana_cost',)})
    def simulate_enter_self_tapped_False(self):
        return self._enter_target('self', tapped=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target'), 'fields': ('mana_cost',)})
    def simulate_enter_self_tapped_True(self):
        return self._enter_target('self', tapped=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_tapped_False(self):
        return self._enter_target('enemy', tapped=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_tapped_True(self):
        return self._enter_target('enemy', tapped=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target'), 'fields': ('mana_cost',)})
    def simulate_enter_none_tapped_False(self):
        return self._enter_target('none', tapped=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target'), 'fields': ('mana_cost',)})
    def simulate_enter_none_tapped_True(self):
        return self._enter_target('none', tapped=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target'), 'fields': ('mana_cost',)})
    def simulate_enter_self_hexproof(self):
        return self._enter_target('self', hexproof=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_hexproof(self):
        return self._enter_target('enemy', hexproof=True)

    @simulate(evidence={'text': ('keyword.flash', 'enter.trigger', 'enter.target'), 'fields': ('mana_cost', 'special_type')})
    def simulate_cast_in_response_window(self):
        return self._enter_target("enemy", in_stack=True)

