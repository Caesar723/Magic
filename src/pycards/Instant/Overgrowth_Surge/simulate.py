from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Overgrowth_Surge.model import Overgrowth_Surge


@bind_card(Overgrowth_Surge)
class Overgrowth_Surge_Simulation(Card_Simulation):
    text_parts = {
        "target.scope": [
            "Choose a target creature you control.",
            "Target one creature you control.",
            "Select a creature you control as the target.",
            "Choose one creature you control to target.",
            "Select a target creature you control.",
            "Choose any creature you control as your target.",
            "Target a creature you control of your choice.",
            "Choose a creature you control as the target for this spell.",
            "Select one creature you control to target.",
            "Choose a creature you control as your target.",
        ],
        "state.effect": [
            "It gets +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "Give it +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "It gains +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "Until your turn ends, it gets +{power_bonus}/+{toughness_bonus}.",
            "Increase its power by {power_bonus} and toughness by {toughness_bonus} until your turn ends.",
            "It receives +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "Its power increases by {power_bonus} and its toughness by {toughness_bonus} until your turn ends.",
            "Grant it +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "It gets an extra {power_bonus} power and {toughness_bonus} toughness until your turn ends.",
            "Until your turn ends, add {power_bonus} to its power and {toughness_bonus} to its toughness.",
        ],
        "keyword.condition": [
            "If its card type or creature type contains \"Treefolk\",",
            "If either of its type labels includes \"Treefolk\",",
            "When \"Treefolk\" occurs in its card type or its creature type,",
            "If its card-type label or creature-type label includes \"Treefolk\",",
            "If \"Treefolk\" appears in either of its type labels,",
            "When the target has \"Treefolk\" in its card type or creature type,",
            "If either its creature type or its card type contains \"Treefolk\",",
            "If one of its card or creature type labels contains \"Treefolk\",",
            "When \"Treefolk\" is present in at least one of its type labels,",
            "If the target's card type or creature type includes \"Treefolk\",",
        ],
        "keyword.effect": [
            "It also gains trample until your turn ends.",
            "It receives trample until your turn ends.",
            "Give it trample until your turn ends.",
            "It has trample until your turn ends.",
            "Until your turn ends, it also has trample.",
            "It gains the trample ability until your turn ends.",
            "Grant it trample until your turn ends.",
            "Until your turn ends, it receives trample.",
            "Until your turn ends, it also gains trample.",
            "It is granted trample until your turn ends.",
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

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_card_type_ready(self):
        return self._target_scene(False, 'Creature - Treefolk', 'Human', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_card_type_tapped(self):
        return self._target_scene(False, 'Creature - Treefolk', 'Human', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_card_type_hexproof(self):
        return self._target_scene(False, 'Creature - Treefolk', 'Human', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_card_type_damaged(self):
        return self._target_scene(False, 'Creature - Treefolk', 'Human', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_type_ready(self):
        return self._target_scene(False, 'Creature - Human', 'Treefolk', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_type_tapped(self):
        return self._target_scene(False, 'Creature - Human', 'Treefolk', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_type_hexproof(self):
        return self._target_scene(False, 'Creature - Human', 'Treefolk', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_type_damaged(self):
        return self._target_scene(False, 'Creature - Human', 'Treefolk', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_multiword_ready(self):
        return self._target_scene(False, 'Creature - Human', 'Creature - Elf Treefolk', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_multiword_tapped(self):
        return self._target_scene(False, 'Creature - Human', 'Creature - Elf Treefolk', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_multiword_hexproof(self):
        return self._target_scene(False, 'Creature - Human', 'Creature - Elf Treefolk', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_self_multiword_damaged(self):
        return self._target_scene(False, 'Creature - Human', 'Creature - Elf Treefolk', False, False, damaged=True)

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

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_card_type_ready(self):
        return self._target_scene(True, 'Creature - Treefolk', 'Human', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_card_type_tapped(self):
        return self._target_scene(True, 'Creature - Treefolk', 'Human', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_card_type_hexproof(self):
        return self._target_scene(True, 'Creature - Treefolk', 'Human', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_card_type_damaged(self):
        return self._target_scene(True, 'Creature - Treefolk', 'Human', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_type_ready(self):
        return self._target_scene(True, 'Creature - Human', 'Treefolk', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_type_tapped(self):
        return self._target_scene(True, 'Creature - Human', 'Treefolk', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_type_hexproof(self):
        return self._target_scene(True, 'Creature - Human', 'Treefolk', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_type_damaged(self):
        return self._target_scene(True, 'Creature - Human', 'Treefolk', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_multiword_ready(self):
        return self._target_scene(True, 'Creature - Human', 'Creature - Elf Treefolk', False, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_multiword_tapped(self):
        return self._target_scene(True, 'Creature - Human', 'Creature - Elf Treefolk', True, False, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_multiword_hexproof(self):
        return self._target_scene(True, 'Creature - Human', 'Creature - Elf Treefolk', False, True, damaged=False)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_multiword_damaged(self):
        return self._target_scene(True, 'Creature - Human', 'Creature - Elf Treefolk', False, False, damaged=True)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.condition', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

