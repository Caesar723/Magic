from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Thornwood_Ranger.model import Thornwood_Ranger


@bind_card(Thornwood_Ranger)
class Thornwood_Ranger_Simulation(Card_Simulation):
    scenario_locks={
        '_enter_target':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
        "keyword.reach": [
            "Reach.",
            "This creature has reach.",
            "{card_name} has reach.",
            "This creature has the reach ability.",
            "{card_name} has the reach ability.",
            "This creature can block creatures with flying.",
            "{card_name} can block creatures with flying.",
            "Reach (This creature can block creatures with flying).",
            "This creature has reach and can block creatures with flying.",
            "{card_name} has reach and can block creatures with flying.",
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
            "Choose another target creature you control.",
            "Select another creature you control as the target.",
            "Target a different creature on your battlefield.",
            "Choose a target from your other creatures.",
            "Select one other creature you control.",
            "Target another creature under your control.",
            "Choose one of your creatures other than this one as the target.",
            "Select a target creature you control, excluding this creature.",
            "Choose a different creature under your control as the target.",
            "Target one of the other creatures on your battlefield.",
        ],
        "enter.effect": [
            "It gets +{power_bonus}/+{toughness_bonus} until its controller's turn ends.",
            "Give it +{power_bonus}/+{toughness_bonus} until its controller's turn ends.",
            "It gains +{power_bonus}/+{toughness_bonus} until its controller's turn ends.",
            "Until its controller's turn ends, it gets +{power_bonus}/+{toughness_bonus}.",
            "Increase its power by {power_bonus} and toughness by {toughness_bonus} until its controller's turn ends.",
            "It receives +{power_bonus}/+{toughness_bonus} until its controller's turn ends.",
            "Its power increases by {power_bonus} and its toughness by {toughness_bonus} until its controller's turn ends.",
            "Grant it +{power_bonus}/+{toughness_bonus} until its controller's turn ends.",
            "It gets an extra {power_bonus} power and {toughness_bonus} toughness until its controller's turn ends.",
            "Until its controller's turn ends, add {power_bonus} to its power and {toughness_bonus} to its toughness.",
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

    @simulate(evidence={'text': ('keyword.reach',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_block_flying_creature(self):
        return self.scenario_combat(True, False, False, enemy_flags={"flying": True})

    def _enter_target(self, role, tapped=False, hexproof=False, in_stack=False):
        self.scenario_prepare()
        subaction = 0
        if role != "none":
            owner = self.player if role == "self" else self.player.opponent
            self.scenario_creature(owner, power=2, health=4, flags={"tap": tapped, "Hexproof": hexproof})
            subaction = 11 if role == "self" else 1
        return self.scenario_cast((subaction,), in_stack=in_stack)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_tapped_False(self):
        return self._enter_target('self', tapped=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_tapped_True(self):
        return self._enter_target('self', tapped=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_tapped_False(self):
        return self._enter_target('enemy', tapped=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_tapped_True(self):
        return self._enter_target('enemy', tapped=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_none_tapped_False(self):
        return self._enter_target('none', tapped=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_none_tapped_True(self):
        return self._enter_target('none', tapped=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_hexproof(self):
        return self._enter_target('self', hexproof=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.target', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_hexproof(self):
        return self._enter_target('enemy', hexproof=True)

