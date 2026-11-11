from game.buffs import Indestructible
from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Oblivion_Devourer.model import Oblivion_Devourer


@bind_card(Oblivion_Devourer)
class Oblivion_Devourer_Simulation(Card_Simulation):
    scenario_locks={
        '_sacrifice_attack':('opponent.battlefield', 'opponent.hand', 'self.battlefield'),
    }

    text_parts = {
        "keyword.menace": [
            "Menace.",
            "This creature has menace.",
            "{card_name} has menace.",
            "This creature carries the menace keyword.",
            "The creature has the menace ability.",
            "Menace is present on this creature.",
            "{card_name} carries the menace keyword.",
            "This creature is marked with menace.",
            "Menace is an ability of this creature.",
            "{card_name} is marked with menace.",
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
            "if you control another creature,",
            "if another creature is on your battlefield,",
            "when you have a creature other than this one in play,",
            "if a different creature is under your control,",
            "provided another creature remains on your battlefield,",
            "when at least one other creature is on your side,",
            "if there is another creature you control,",
            "if one of your other creatures is available,",
            "when your battlefield contains a creature besides this one,",
            "if you have another friendly creature in play,",
        ],
        "attack.effect": [
            "destroy the first other friendly creature with the smallest current power plus remaining health, then randomly remove {discard_count} opposing hand cards, or all if fewer remain.",
            "choose the first other friendly creature minimizing current power plus remaining health, destroy it, and randomly remove up to {discard_count} opposing hand cards, taking all if fewer.",
            "destroy the earliest other friendly creature with minimum power-plus-current-health, then remove {discard_count} random cards from the opposing hand if available.",
            "destroy your first other creature with the lowest current power-and-health sum and randomly take {discard_count} opposing hand cards out, limited by availability.",
            "find your first other creature with minimum current power plus remaining health, destroy it, and randomly remove {discard_count} cards from your opponent's hand if available.",
            "destroy the first minimum-sum creature among your others, using current power plus health, then randomly remove {discard_count} opposing hand cards or all if fewer exist.",
            "take your first other creature minimizing power plus remaining health, destroy it, and randomly remove as many as {discard_count} opposing hand cards.",
            "destroy the first other friendly creature with the smallest current power-health total and remove random opposing hand cards up to {discard_count}, taking all if fewer.",
            "destroy your earliest other creature with the lowest current power plus remaining health, then randomly remove {discard_count} cards from the opposing hand when available.",
            "destroy the first other creature on your side minimizing current power plus health, then randomly remove {discard_count} opposing hand cards, limited by availability.",
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect')})
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

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _sacrifice_attack(self, count, hand_count, blocked=False, protected=False, tied=False):
        record = self.scenario_unblocked(blocked)
        if blocked:
            self.player.opponent.battlefield[0].power = self.player.opponent.battlefield[0].actual_power = 2
            self.player.opponent.battlefield[0].live = self.player.opponent.battlefield[0].actual_live = self.card.state[0] + 1
            self.scenario_block()
        for index in range(count):
            creature = self.scenario_creature(self.player, power=1 if tied else index + 1, health=1 if tied else index + 2, flags={})
            if protected:
                self.scenario_buff(creature, Indestructible(self.card, creature))
        self.scenario_clear(self.player.opponent,"hand")
        self.scenario_random_cards(self.player.opponent,"hand",hand_count)
        self.player.opponent.hand = [card for card in self.player.opponent.hand if card.type == "Instant"][:hand_count]
        return record

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_0_hand_empty_blocked_False(self):
        return self._sacrifice_attack(0, 0, False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_0_hand_empty_blocked_True(self):
        return self._sacrifice_attack(0, 0, True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_0_hand_short_blocked_False(self):
        return self._sacrifice_attack(0, 1, False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_0_hand_short_blocked_True(self):
        return self._sacrifice_attack(0, 1, True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_0_hand_exact_blocked_False(self):
        return self._sacrifice_attack(0, self.card.effect_params["discard_count"], False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_0_hand_exact_blocked_True(self):
        return self._sacrifice_attack(0, self.card.effect_params["discard_count"], True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_0_hand_plenty_blocked_False(self):
        return self._sacrifice_attack(0, self.card.effect_params["discard_count"] * 3, False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_0_hand_plenty_blocked_True(self):
        return self._sacrifice_attack(0, self.card.effect_params["discard_count"] * 3, True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_1_hand_empty_blocked_False(self):
        return self._sacrifice_attack(1, 0, False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_1_hand_empty_blocked_True(self):
        return self._sacrifice_attack(1, 0, True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_1_hand_short_blocked_False(self):
        return self._sacrifice_attack(1, 1, False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_1_hand_short_blocked_True(self):
        return self._sacrifice_attack(1, 1, True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_1_hand_exact_blocked_False(self):
        return self._sacrifice_attack(1, self.card.effect_params["discard_count"], False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_1_hand_exact_blocked_True(self):
        return self._sacrifice_attack(1, self.card.effect_params["discard_count"], True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_1_hand_plenty_blocked_False(self):
        return self._sacrifice_attack(1, self.card.effect_params["discard_count"] * 3, False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_1_hand_plenty_blocked_True(self):
        return self._sacrifice_attack(1, self.card.effect_params["discard_count"] * 3, True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_3_hand_empty_blocked_False(self):
        return self._sacrifice_attack(3, 0, False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_3_hand_empty_blocked_True(self):
        return self._sacrifice_attack(3, 0, True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_3_hand_short_blocked_False(self):
        return self._sacrifice_attack(3, 1, False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_3_hand_short_blocked_True(self):
        return self._sacrifice_attack(3, 1, True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_3_hand_exact_blocked_False(self):
        return self._sacrifice_attack(3, self.card.effect_params["discard_count"], False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_3_hand_exact_blocked_True(self):
        return self._sacrifice_attack(3, self.card.effect_params["discard_count"], True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_3_hand_plenty_blocked_False(self):
        return self._sacrifice_attack(3, self.card.effect_params["discard_count"] * 3, False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_allies_3_hand_plenty_blocked_True(self):
        return self._sacrifice_attack(3, self.card.effect_params["discard_count"] * 3, True)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_minimum_protected(self):
        return self._sacrifice_attack(3, 5, True, True, False)

    @simulate(evidence={'text': ('keyword.menace', 'attack.trigger', 'attack.condition', 'attack.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_minimum_tied(self):
        return self._sacrifice_attack(3, 5, True, False, True)

