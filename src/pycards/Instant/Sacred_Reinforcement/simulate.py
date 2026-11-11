from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Sacred_Reinforcement.model import Sacred_Reinforcement


@bind_card(Sacred_Reinforcement)
class Sacred_Reinforcement_Simulation(Card_Simulation):
    text_parts = {
        "target.scope": [
            "Choose a target creature your opponent controls.",
            "Target one creature your opponent controls.",
            "Select a creature your opponent controls as the target.",
            "Choose one creature your opponent controls to target.",
            "Select a target creature your opponent controls.",
            "Choose any creature your opponent controls as your target.",
            "Target a creature your opponent controls of your choice.",
            "Choose a creature your opponent controls as the target for this spell.",
            "Select one creature your opponent controls to target.",
            "Choose a creature your opponent controls as your target.",
        ],
        "tap.effect": [
            "Tap that creature and prevent it from untapping until its controller's turn ends, then untap it.",
            "The target becomes tapped, cannot be untapped for the rest of the turn, and untaps when its controller's turn ends.",
            "Tap the target, keep it from untapping this turn, and untap it when its controller's turn ends.",
            "Tap the chosen creature. It cannot be untapped until its controller's turn ends, when it untaps.",
            "The chosen creature becomes tapped and is unable to untap until its controller's turn ends, then becomes untapped.",
            "Tap that creature, block any untapping until turn end, and then untap it.",
            "Cause the target to become tapped and remain unable to untap until its controller's turn ends, then untap it.",
            "The target becomes tapped and cannot be untapped before its controller's turn ends, then it untaps.",
            "Tap the selected creature, prevent it from untapping until its controller's turn ends, and untap it when its controller's turn ends.",
            "The selected creature is tapped, is prevented from untapping until its controller's turn ends, and untaps when its controller's turn ends.",
        ],
        "state.effect": [
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
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _target_scene(self, opponent, card_type="Creature - Human", creature_type="Human", tapped=False, hexproof=False, offset=1, damaged=False):
        self.scenario_prepare()
        owner = self.player.opponent if opponent else self.player
        health = self.card.effect_params.get("toughness_reduction", 2) + offset
        if health <= 0:
            return self.scenario_skip()
        target = self.scenario_creature(owner, power=2, health=health, flags={"tap": tapped, "Hexproof": hexproof})
        target.type_card, target.type_creature = card_type, creature_type
        if damaged:
            target.live = health + 3
        self.scenario_creature(owner.opponent, power=1, health=5, flags={})
        subaction = 1 if opponent else 11
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('target.scope', 'tap.effect', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_normal_ready(self):
        return self._target_scene(False, 'Creature - Human', 'Human', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'tap.effect', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_normal_tapped(self):
        return self._target_scene(False, 'Creature - Human', 'Human', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'tap.effect', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_normal_hexproof(self):
        return self._target_scene(False, 'Creature - Human', 'Human', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'tap.effect', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_normal_damaged(self):
        return self._target_scene(False, 'Creature - Human', 'Human', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'tap.effect', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_ready(self):
        return self._target_scene(True, 'Creature - Human', 'Human', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'tap.effect', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_tapped(self):
        return self._target_scene(True, 'Creature - Human', 'Human', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'tap.effect', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_hexproof(self):
        return self._target_scene(True, 'Creature - Human', 'Human', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'tap.effect', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_damaged(self):
        return self._target_scene(True, 'Creature - Human', 'Human', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'tap.effect', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

