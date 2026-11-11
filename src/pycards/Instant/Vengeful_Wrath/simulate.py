from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.Instant.Vengeful_Wrath.model import Vengeful_Wrath


@bind_card(Vengeful_Wrath)
class Vengeful_Wrath_Simulation(Card_Simulation):
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
        "remove.effect": [
            "Destroy that creature.",
            "Destroy the targeted creature.",
            "Destroy the creature you chose.",
            "That creature is destroyed.",
            "The selected creature is destroyed.",
            "Destroy your chosen creature.",
            "Cause that creature to be destroyed.",
            "Destroy the chosen target.",
            "Have the targeted creature destroyed.",
            "Destroy the creature selected this way.",
        ],
        "splash.condition": [
            "If your opponent currently has a creature on the battlefield,",
            "If an opposing creature is currently available,",
            "When your opponent has any creatures in play,",
            "If the opposing battlefield is not empty,",
            "If your opponent still has a creature in play,",
            "When an opposing creature remains available,",
            "If any creatures are currently under your opponent's control,",
            "If there is a creature on the opposing battlefield,",
            "When a creature is present on your opponent's battlefield,",
            "If at least one opposing creature is in play,",
        ],
        "splash.effect": [
            "deal damage equal to the original target's power before destruction to a random opposing creature, which may be the marked target before cleanup.",
            "pick an opposing creature at random, including the marked target before cleanup, and deal damage equal to the original target's earlier power.",
            "deal the target's pre-destruction power as damage to a random opposing creature, allowing the marked target before cleanup.",
            "inflict damage equal to the original target's power on a random opposing creature, with the marked target still eligible until cleanup.",
            "choose any opposing creature randomly, including the marked original target until cleanup, and deal damage matching that target's power.",
            "hit a random opposing creature for the original target's pre-destruction power, even if that random choice is the marked target awaiting cleanup.",
            "deal damage matching the first target's power to a random opposing creature, including that target before destruction cleanup.",
            "pick a random opposing creature from the current battlefield and deal damage equal to the first target's earlier power, with the marked target still included.",
            "deal the first target's pre-destruction power in damage to a random opposing creature, allowing a repeat hit on the marked target until cleanup.",
            "select an opposing creature randomly from those still on the battlefield, including the marked target before cleanup, and deal damage equal to the first target's power.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _target_scene(self, opponent, flags=None, power=3, current_power=None, health=5, missing=1, protected=False, enemy_count=1):
        self.scenario_prepare()
        owner = self.player.opponent if opponent else self.player
        target = self.scenario_creature(owner, power=power, health=health, flags=flags or {})
        if current_power is not None:
            target.actual_power = current_power
        if protected:
            target.gain_buff(Indestructible(self.card, target), self.card)
        self.player.life = max(1, self.player.ini_life - missing)
        for index in range(enemy_count):
            self.scenario_creature(self.player.opponent, power=1, health=max(1, power + index - 1), flags={})
        subaction = 1 if opponent else 11
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_ready(self):
        return self._target_scene(False, {})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tapped(self):
        return self._target_scene(False, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_flying(self):
        return self._target_scene(False, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._target_scene(False, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_indestructible(self):
        return self._target_scene(False, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_splash_candidates(self):
        return self._target_scene(False, enemy_count=0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_splash_candidates(self):
        return self._target_scene(False, enemy_count=1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_splash_candidates(self):
        return self._target_scene(False, enemy_count=3)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_ready(self):
        return self._target_scene(True, {})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tapped(self):
        return self._target_scene(True, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_flying(self):
        return self._target_scene(True, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(True, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_indestructible(self):
        return self._target_scene(True, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_0_splash_candidates(self):
        return self._target_scene(True, enemy_count=0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_1_splash_candidates(self):
        return self._target_scene(True, enemy_count=1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_3_splash_candidates(self):
        return self._target_scene(True, enemy_count=3)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

