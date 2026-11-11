from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Shadowform_Surge.model import Shadowform_Surge


@bind_card(Shadowform_Surge)
class Shadowform_Surge_Simulation(Card_Simulation):
    scenario_locks={
        '_target_scene':('opponent.battlefield', 'self.battlefield'),
        'simulate_no_creatures':('opponent.battlefield', 'self.battlefield'),
    }

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
        "state.effect": [
            "It gets -{power_reduction}/-{toughness_reduction} until its controller's turn ends.",
            "Give it -{power_reduction}/-{toughness_reduction} until its controller's turn ends.",
            "It receives -{power_reduction}/-{toughness_reduction} until its controller's turn ends.",
            "Until its controller's turn ends, it gets -{power_reduction}/-{toughness_reduction}.",
            "Reduce its power by {power_reduction} and toughness by {toughness_reduction} until its controller's turn ends.",
            "It suffers -{power_reduction}/-{toughness_reduction} until its controller's turn ends.",
            "Its power falls by {power_reduction} and its toughness by {toughness_reduction} until its controller's turn ends.",
            "Apply -{power_reduction}/-{toughness_reduction} to it until its controller's turn ends.",
            "It loses {power_reduction} power and {toughness_reduction} toughness until its controller's turn ends.",
            "Until its controller's turn ends, subtract {power_reduction} from its power and {toughness_reduction} from its toughness.",
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

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_normal_ready(self):
        return self._target_scene(False, 'Creature - Human', 'Human', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_normal_tapped(self):
        return self._target_scene(False, 'Creature - Human', 'Human', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_normal_hexproof(self):
        return self._target_scene(False, 'Creature - Human', 'Human', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_normal_damaged(self):
        return self._target_scene(False, 'Creature - Human', 'Human', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_below_lethal(self):
        return self._target_scene(False, offset=-1)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_equal_lethal(self):
        return self._target_scene(False, offset=0)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_self_above_lethal(self):
        return self._target_scene(False, offset=1)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_ready(self):
        return self._target_scene(True, 'Creature - Human', 'Human', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_tapped(self):
        return self._target_scene(True, 'Creature - Human', 'Human', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_hexproof(self):
        return self._target_scene(True, 'Creature - Human', 'Human', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_damaged(self):
        return self._target_scene(True, 'Creature - Human', 'Human', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_below_lethal(self):
        return self._target_scene(True, offset=-1)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_equal_lethal(self):
        return self._target_scene(True, offset=0)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_above_lethal(self):
        return self._target_scene(True, offset=1)

    @simulate(evidence={'text': ('target.scope', 'state.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

