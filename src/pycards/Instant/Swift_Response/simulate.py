from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.Instant.Swift_Response.model import Swift_Response


@bind_card(Swift_Response)
class Swift_Response_Simulation(Card_Simulation):
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
            "If its base power is at most {power_threshold},",
            "If the target's base power is {power_threshold} or less,",
            "When its printed power is no greater than {power_threshold},",
            "If the creature's base power does not exceed {power_threshold},",
            "If that creature has base power of at most {power_threshold},",
            "When the target's base power is equal to or below {power_threshold},",
            "If its base power is no higher than {power_threshold},",
            "If the selected creature's base power is at most {power_threshold},",
            "When the chosen creature has {power_threshold} or less base power,",
            "If the target has base power no greater than {power_threshold},",
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
            target.gain_buff(Indestructible(self.card, target), self.card)
        self.player.life = max(1, self.player.ini_life - missing)
        subaction = 1 if opponent else 11
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_ready(self):
        return self._target_scene(False, {})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tapped(self):
        return self._target_scene(False, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_flying(self):
        return self._target_scene(False, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._target_scene(False, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_indestructible(self):
        return self._target_scene(False, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_base_power_below(self):
        return self._target_scene(False, power=max(0, self.card.effect_params["power_threshold"] + -1))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_base_power_equal(self):
        return self._target_scene(False, power=max(0, self.card.effect_params["power_threshold"] + 0))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_base_power_above(self):
        return self._target_scene(False, power=max(0, self.card.effect_params["power_threshold"] + 1))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_base_low_current_high(self):
        return self._target_scene(False, power=max(0, self.card.effect_params["power_threshold"] - 1), current_power=self.card.effect_params["power_threshold"] + 2)

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_base_high_current_low(self):
        return self._target_scene(False, power=self.card.effect_params["power_threshold"] + 1, current_power=max(0, self.card.effect_params["power_threshold"] - 1))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_ready(self):
        return self._target_scene(True, {})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tapped(self):
        return self._target_scene(True, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_flying(self):
        return self._target_scene(True, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(True, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_indestructible(self):
        return self._target_scene(True, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_base_power_below(self):
        return self._target_scene(True, power=max(0, self.card.effect_params["power_threshold"] + -1))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_base_power_equal(self):
        return self._target_scene(True, power=max(0, self.card.effect_params["power_threshold"] + 0))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_base_power_above(self):
        return self._target_scene(True, power=max(0, self.card.effect_params["power_threshold"] + 1))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_base_low_current_high(self):
        return self._target_scene(True, power=max(0, self.card.effect_params["power_threshold"] - 1), current_power=self.card.effect_params["power_threshold"] + 2)

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_base_high_current_low(self):
        return self._target_scene(True, power=self.card.effect_params["power_threshold"] + 1, current_power=max(0, self.card.effect_params["power_threshold"] - 1))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

