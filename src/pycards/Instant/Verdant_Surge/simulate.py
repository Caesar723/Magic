from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Verdant_Surge.model import Verdant_Surge


@bind_card(Verdant_Surge)
class Verdant_Surge_Simulation(Card_Simulation):
    scenario_locks={
        '_target_scene':('opponent.battlefield', 'self.battlefield'),
        'simulate_no_creatures':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
        "target.scope": [
            "Choose a target creature.",
            "Target one creature.",
            "Select a creature as the target.",
            "Choose one creature to target.",
            "Select a target creature.",
            "Choose any creature as your target.",
            "Target a creature of your choice.",
            "Choose a creature as the target for this spell.",
            "Select one creature to target.",
            "Choose a creature as your target.",
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
        "keyword.condition": [
            "If its creature-type label is exactly \"Druid\",",
            "If its creature type equals \"Druid\",",
            "When its creature-type label is \"Druid\" exactly,",
            "If the target's creature type is the exact text \"Druid\",",
            "If its complete creature-type label is \"Druid\",",
            "When the target has precisely \"Druid\" as its creature type,",
            "If the whole creature-type label reads \"Druid\",",
            "If its creature-type text matches \"Druid\" exactly,",
            "When its creature type is exactly the label \"Druid\",",
            "If the target's entire creature type is \"Druid\",",
        ],
        "keyword.effect": [
            "It also gains reach until its controller's turn ends.",
            "It receives reach until its controller's turn ends.",
            "Give it reach until its controller's turn ends.",
            "It has reach until its controller's turn ends.",
            "Until its controller's turn ends, it also has reach.",
            "It gains the reach ability until its controller's turn ends.",
            "Grant it reach until its controller's turn ends.",
            "Until its controller's turn ends, it receives reach.",
            "Until its controller's turn ends, it also gains reach.",
            "It is granted reach until its controller's turn ends.",
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

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_normal_ready(self):
        return self._target_scene(False, 'Creature - Human', 'Human', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_normal_tapped(self):
        return self._target_scene(False, 'Creature - Human', 'Human', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_normal_hexproof(self):
        return self._target_scene(False, 'Creature - Human', 'Human', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_normal_damaged(self):
        return self._target_scene(False, 'Creature - Human', 'Human', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_card_type_ready(self):
        return self._target_scene(False, 'Creature - Druid', 'Human', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_card_type_tapped(self):
        return self._target_scene(False, 'Creature - Druid', 'Human', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_card_type_hexproof(self):
        return self._target_scene(False, 'Creature - Druid', 'Human', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_card_type_damaged(self):
        return self._target_scene(False, 'Creature - Druid', 'Human', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_type_ready(self):
        return self._target_scene(False, 'Creature - Human', 'Druid', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_type_tapped(self):
        return self._target_scene(False, 'Creature - Human', 'Druid', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_type_hexproof(self):
        return self._target_scene(False, 'Creature - Human', 'Druid', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_type_damaged(self):
        return self._target_scene(False, 'Creature - Human', 'Druid', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_multiword_ready(self):
        return self._target_scene(False, 'Creature - Human', 'Creature - Elf Druid', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_multiword_tapped(self):
        return self._target_scene(False, 'Creature - Human', 'Creature - Elf Druid', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_multiword_hexproof(self):
        return self._target_scene(False, 'Creature - Human', 'Creature - Elf Druid', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_self_multiword_damaged(self):
        return self._target_scene(False, 'Creature - Human', 'Creature - Elf Druid', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_ready(self):
        return self._target_scene(True, 'Creature - Human', 'Human', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_tapped(self):
        return self._target_scene(True, 'Creature - Human', 'Human', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_hexproof(self):
        return self._target_scene(True, 'Creature - Human', 'Human', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal_damaged(self):
        return self._target_scene(True, 'Creature - Human', 'Human', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_card_type_ready(self):
        return self._target_scene(True, 'Creature - Druid', 'Human', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_card_type_tapped(self):
        return self._target_scene(True, 'Creature - Druid', 'Human', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_card_type_hexproof(self):
        return self._target_scene(True, 'Creature - Druid', 'Human', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_card_type_damaged(self):
        return self._target_scene(True, 'Creature - Druid', 'Human', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_type_ready(self):
        return self._target_scene(True, 'Creature - Human', 'Druid', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_type_tapped(self):
        return self._target_scene(True, 'Creature - Human', 'Druid', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_type_hexproof(self):
        return self._target_scene(True, 'Creature - Human', 'Druid', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_type_damaged(self):
        return self._target_scene(True, 'Creature - Human', 'Druid', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_multiword_ready(self):
        return self._target_scene(True, 'Creature - Human', 'Creature - Elf Druid', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_multiword_tapped(self):
        return self._target_scene(True, 'Creature - Human', 'Creature - Elf Druid', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_multiword_hexproof(self):
        return self._target_scene(True, 'Creature - Human', 'Creature - Elf Druid', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_multiword_damaged(self):
        return self._target_scene(True, 'Creature - Human', 'Creature - Elf Druid', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

