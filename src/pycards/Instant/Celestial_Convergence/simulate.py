from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.Instant.Celestial_Convergence.model import Celestial_Convergence


@bind_card(Celestial_Convergence)
class Celestial_Convergence_Simulation(Card_Simulation):
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
        "remove.effect": [
            "Exile that creature.",
            "Exile the targeted creature.",
            "Exile the creature you chose.",
            "That creature is exiled.",
            "The selected creature is exiled.",
            "Exile your chosen creature.",
            "Cause that creature to be exiled.",
            "Exile the chosen target.",
            "Have the targeted creature exiled.",
            "Exile the creature selected this way.",
        ],
        "heal.condition": [
            "If the target's mana value is at most {mana_threshold},",
            "If its total mana cost is {mana_threshold} or less,",
            "When the sum of its mana costs is no greater than {mana_threshold},",
            "If the creature's mana value does not exceed {mana_threshold},",
            "If that creature has a total mana value of at most {mana_threshold},",
            "When the target's mana value is equal to or below {mana_threshold},",
            "If its total mana cost is no higher than {mana_threshold},",
            "If the selected creature's mana value is at most {mana_threshold},",
            "When the chosen creature has a mana value of {mana_threshold} or less,",
            "If its total mana value is no greater than {mana_threshold},",
        ],
        "heal.effect": [
            "You gain life equal to the target's mana value.",
            "Gain an amount of life matching that creature's total mana cost.",
            "You restore life equal to the selected creature's mana value.",
            "Increase your life total by that creature's total mana value.",
            "Gain as much life as the total mana cost of the creature you exiled.",
            "You gain life equal to the sum of the target's mana costs.",
            "Restore to yourself an amount of life equal to its mana value.",
            "Gain life matching the exiled creature's total mana cost.",
            "You gain life determined by that creature's total mana value.",
            "The target's total mana cost is the amount of life you gain.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _target_scene(self, opponent, flags=None, power=3, current_power=None, health=5, missing=1, protected=False, mana_offset=0):
        self.scenario_prepare()
        owner = self.player.opponent if opponent else self.player
        target = self.scenario_creature(owner, power=power, health=health, flags=flags or {})
        if current_power is not None:
            target.actual_power = current_power
        if protected:
            self.scenario_buff(target, Indestructible(self.card, target))
        self.player.life = max(1, self.player.ini_life - missing)
        target.mana_cost = str(max(0, self.card.effect_params["mana_threshold"] + mana_offset))
        subaction = 1 if opponent else 11
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_ready(self):
        return self._target_scene(False, {})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tapped(self):
        return self._target_scene(False, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_flying(self):
        return self._target_scene(False, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._target_scene(False, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_indestructible(self):
        return self._target_scene(False, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_mana_below(self):
        return self._target_scene(False, mana_offset=-1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_mana_equal(self):
        return self._target_scene(False, mana_offset=0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_mana_above(self):
        return self._target_scene(False, mana_offset=1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_healing_full(self):
        return self._target_scene(False, missing=0, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_healing_near_full(self):
        return self._target_scene(False, missing=1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_healing_injured(self):
        return self._target_scene(False, missing=self.player.ini_life - 1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_ready(self):
        return self._target_scene(True, {})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tapped(self):
        return self._target_scene(True, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_flying(self):
        return self._target_scene(True, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(True, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_indestructible(self):
        return self._target_scene(True, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_mana_below(self):
        return self._target_scene(True, mana_offset=-1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_mana_equal(self):
        return self._target_scene(True, mana_offset=0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_mana_above(self):
        return self._target_scene(True, mana_offset=1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_healing_full(self):
        return self._target_scene(True, missing=0, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_healing_near_full(self):
        return self._target_scene(True, missing=1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_healing_injured(self):
        return self._target_scene(True, missing=self.player.ini_life - 1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.condition', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

