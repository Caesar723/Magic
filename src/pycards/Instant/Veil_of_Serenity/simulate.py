from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.Instant.Veil_of_Serenity.model import Veil_of_Serenity


@bind_card(Veil_of_Serenity)
class Veil_of_Serenity_Simulation(Card_Simulation):
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

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_ready(self):
        return self._target_scene(False, {})

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tapped(self):
        return self._target_scene(False, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_flying(self):
        return self._target_scene(False, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._target_scene(False, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_indestructible(self):
        return self._target_scene(False, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_ready(self):
        return self._target_scene(True, {})

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tapped(self):
        return self._target_scene(True, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_flying(self):
        return self._target_scene(True, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(True, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_indestructible(self):
        return self._target_scene(True, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

