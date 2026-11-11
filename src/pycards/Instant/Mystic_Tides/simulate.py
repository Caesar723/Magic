from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Mystic_Tides.model import Mystic_Tides


@bind_card(Mystic_Tides)
class Mystic_Tides_Simulation(Card_Simulation):
    text_parts = {
        "cast.condition": [
            "You can cast this only with at least {mana_threshold} available mana, in addition to being able to pay its normal cost.",
            "Casting this requires at least {mana_threshold} available mana and payment of its normal mana cost.",
            "This can be cast only if your available mana totals at least {mana_threshold} and you can pay its cost.",
            "To cast this, have at least {mana_threshold} available mana and pay its ordinary cost.",
            "You need at least {mana_threshold} available mana to cast this, as well as enough to pay its normal cost.",
            "Cast this only when at least {mana_threshold} mana is available and its mana cost can be paid.",
            "Casting is allowed only with {mana_threshold} or more available mana and an affordable normal cost.",
            "Have at least {mana_threshold} available mana and pay the normal cost to cast this.",
            "This requires at least {mana_threshold} mana available before casting and payment of the normal cost.",
            "Cast this only if you have at least {mana_threshold} available mana and can cover its usual cost.",
        ],
        "counter.effect": [
            "Counter the nonland spell on top of the stack.",
            "Counter the top spell on the stack if it is not a land.",
            "Remove the top nonland spell from the stack without resolving it.",
            "Counter the nonland spell currently on top of the stack.",
            "Stop the top nonland spell on the stack from resolving.",
            "Counter the spell at the top of the stack, excluding lands.",
            "Cancel the nonland spell at the top of the stack.",
            "Counter the topmost spell on the stack if it is not a land.",
            "Prevent the nonland spell on top of the stack from resolving.",
            "Counter the current top spell on the stack, provided it is not a land.",
        ],
        "tap.selection": [
            "Choose two opposing creatures independently at random, allowing both choices to be the same creature.",
            "Randomly choose an opposing creature twice, with each choice independent and repetition allowed.",
            "Pick two opposing creatures at random with replacement.",
            "Make two independent random choices among opposing creatures, allowing the same creature twice.",
            "Select an opposing creature at random, then independently select another from the same set.",
            "Randomly select two opposing creatures in order, allowing a repeated selection.",
            "Choose an opposing creature randomly two times, keeping both choices independent.",
            "Pick one opposing creature at random and then make a second independent choice from all opposing creatures.",
            "Randomly choose a first and a second opposing creature, with repeats permitted.",
            "Make two random selections from the opposing creatures, choosing independently each time.",
        ],
        "tap.effect": [
            "Tap the second creature and prevent it from untapping. When your opponent's turn ends, untap the first creature. Remove the lock only if both selections were the same creature.",
            "The second selected creature is tapped and locked against untapping. Untap the first when your opponent's turn ends, releasing the lock only when both choices matched.",
            "Tap and lock the second creature against untapping, then untap the first when your opponent's turn ends. The lock expires only if both choices selected the same creature.",
            "The second choice becomes tapped and cannot be untapped. When your opponent's turn ends, untap the first choice and remove the lock only if it was also the second choice.",
            "Lock the second creature tapped. When your opponent's turn ends, untap the first creature and release the lock only for a matching pair of selections.",
            "Tap the second selected creature and stop it from untapping. The first untaps when your opponent's turn ends, and the lock ends only if the selections matched.",
            "Apply a tap lock to the second choice, untap the first when your opponent's turn ends, and release the lock only when both choices were the same creature.",
            "The second creature is tapped with an untap lock. When your opponent's turn ends, untap the first, clearing that lock only if the same creature was chosen twice.",
            "Tap the second creature and lock its untapping. Untap the first when your opponent's turn ends, removing the lock only if it was also the second creature.",
            "Prevent the second creature from untapping after tapping it. When your opponent's turn ends, untap the first and clear the lock only when both selected objects were identical.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    def _tap_scene(self, count, own_target=False):
        self.scenario_prepare()
        self.scenario_stack("instant", own_target)
        for _ in range(count):
            self.scenario_creature(self.player.opponent, flags={})
        if not count:
            return self.scenario_skip()
        extra = max(0, self.card.effect_params["mana_threshold"] - sum(self.card.cost.values()))
        return self.scenario_cast(in_stack=True, extra_cost={"colorless": extra})

    @simulate(evidence={'text': ('cast.condition', 'counter.effect', 'tap.selection', 'tap.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_spell_0_creatures(self):
        return self._tap_scene(0, False)

    @simulate(evidence={'text': ('cast.condition', 'counter.effect', 'tap.selection', 'tap.effect'), 'fields': ('mana_cost',)})
    def simulate_self_spell_0_creatures(self):
        return self._tap_scene(0, True)

    @simulate(evidence={'text': ('cast.condition', 'counter.effect', 'tap.selection', 'tap.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_spell_1_creatures(self):
        return self._tap_scene(1, False)

    @simulate(evidence={'text': ('cast.condition', 'counter.effect', 'tap.selection', 'tap.effect'), 'fields': ('mana_cost',)})
    def simulate_self_spell_1_creatures(self):
        return self._tap_scene(1, True)

    @simulate(evidence={'text': ('cast.condition', 'counter.effect', 'tap.selection', 'tap.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_spell_3_creatures(self):
        return self._tap_scene(3, False)

    @simulate(evidence={'text': ('cast.condition', 'counter.effect', 'tap.selection', 'tap.effect'), 'fields': ('mana_cost',)})
    def simulate_self_spell_3_creatures(self):
        return self._tap_scene(3, True)

    @simulate(evidence={'text': ('cast.condition',), 'fields': ('mana_cost',)})
    def simulate_below_own_mana_threshold(self):
        self.scenario_prepare()
        self.scenario_stack()
        self.scenario_creature(self.player.opponent, flags={})
        self.card.mana_cost = "U"
        if self.card.effect_params["mana_threshold"] <= 1:
            return self.scenario_skip()
        return self.scenario_cast(in_stack=True)

