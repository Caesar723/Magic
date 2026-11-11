from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.Instant.Avenging_Light.model import Avenging_Light


@bind_card(Avenging_Light)
class Avenging_Light_Simulation(Card_Simulation):
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
        "heal.effect": [
            "You gain life equal to that creature's power.",
            "Gain an amount of life equal to the selected creature's power.",
            "You restore life equal to that creature's power.",
            "Increase your life total by the power of that creature.",
            "Gain life matching the power of the creature you chose.",
            "You gain an amount of life matching that creature's power.",
            "Restore to yourself an amount of life equal to that creature's power.",
            "Gain as much life as the power of that selected creature.",
            "The selected creature's power determines how much life you gain.",
            "You gain life matching the selected creature's power.",
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

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_ready(self):
        return self._target_scene(False, {})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tapped(self):
        return self._target_scene(False, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_flying(self):
        return self._target_scene(False, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._target_scene(False, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_indestructible(self):
        return self._target_scene(False, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_healing_full(self):
        return self._target_scene(False, missing=0, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_healing_near_full(self):
        return self._target_scene(False, missing=1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_healing_injured(self):
        return self._target_scene(False, missing=self.player.ini_life - 1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_ready(self):
        return self._target_scene(True, {})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tapped(self):
        return self._target_scene(True, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_flying(self):
        return self._target_scene(True, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(True, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_indestructible(self):
        return self._target_scene(True, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_healing_full(self):
        return self._target_scene(True, missing=0, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_healing_near_full(self):
        return self._target_scene(True, missing=1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_healing_injured(self):
        return self._target_scene(True, missing=self.player.ini_life - 1, flags={"flying": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

