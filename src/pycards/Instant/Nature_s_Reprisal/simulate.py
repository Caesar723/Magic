from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.Instant.Nature_s_Reprisal.model import Nature_s_Reprisal


@bind_card(Nature_s_Reprisal)
class Nature_s_Reprisal_Simulation(Card_Simulation):
    scenario_locks={
        '_target_scene':('opponent.battlefield', 'self.battlefield'),
        'simulate_no_creatures':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
        "target.scope": [
            "Choose a target opposing creature.",
            "Target one opposing creature.",
            "Select a opposing creature as the target.",
            "Choose one opposing creature to target.",
            "Select a target opposing creature.",
            "Choose any opposing creature as your target.",
            "Target a opposing creature of your choice.",
            "Choose a opposing creature as the target for this spell.",
            "Select one opposing creature to target.",
            "Choose a opposing creature as your target.",
        ],
        "destroy.condition": [
            "If the target has flying,",
            "If that creature has flying,",
            "When the chosen creature has flying,",
            "If the selected creature has the flying ability,",
            "If you chose a creature with flying,",
            "When your target has the flying ability,",
            "If the targeted creature is a flyer,",
            "If the chosen target has flying,",
            "When that creature has the flying ability,",
            "If that creature is flying,",
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
        "heal.effect": [
            "you gain {heal} life.",
            "gain {heal} life.",
            "you gain a total of {heal} life.",
            "gain a total of {heal} life.",
            "increase your life total by {heal}.",
            "you increase your life total by {heal}.",
            "restore {heal} life.",
            "you restore {heal} life.",
            "gain an amount of life equal to {heal}.",
            "you gain an amount of life equal to {heal}.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _target_scene(self, opponent, flags=None, power=3, current_power=None, health=5, missing=1, protected=False):
        self.scenario_prepare()
        owner = self.player.opponent if opponent else self.player
        target = self.scenario_creature(owner, power=power, health=health, flags=flags or {})
        if current_power is not None:
            target.actual_power = current_power
        if protected:
            self.scenario_buff(target, Indestructible(self.card, target))
        self.player.life = max(1, self.player.ini_life - missing)
        subaction = 1 if opponent else 11
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_ready(self):
        return self._target_scene(False, {})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tapped(self):
        return self._target_scene(False, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_flying(self):
        return self._target_scene(False, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._target_scene(False, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_indestructible(self):
        return self._target_scene(False, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_healing_full(self):
        return self._target_scene(False, missing=0, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_healing_near_full(self):
        return self._target_scene(False, missing=1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_healing_injured(self):
        return self._target_scene(False, missing=self.player.ini_life - 1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_ready(self):
        return self._target_scene(True, {})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tapped(self):
        return self._target_scene(True, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_flying(self):
        return self._target_scene(True, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(True, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_indestructible(self):
        return self._target_scene(True, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_healing_full(self):
        return self._target_scene(True, missing=0, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_healing_near_full(self):
        return self._target_scene(True, missing=1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_healing_injured(self):
        return self._target_scene(True, missing=self.player.ini_life - 1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

