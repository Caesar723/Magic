from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.sorcery.Celestial_Purge.model import Celestial_Purge


@bind_card(Celestial_Purge)
class Celestial_Purge_Simulation(Card_Simulation):
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
        "exile.condition": [
            "If its color attribute is exactly black or red,",
            "If its color is labeled precisely black or red,",
            "When its color label is either black or red,",
            "If the target's color attribute equals black or red,",
            "If its color label is black or its color label is red,",
            "When the selected creature has exactly black or red as its color label,",
            "If the chosen creature's color attribute is one of black and red,",
            "If that creature's color label is exactly red or black,",
            "When the target is labeled black or red in its color attribute,",
            "If its exact color label is red or black,",
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

    def _target_scene(self, opponent, flags=None, power=3, current_power=None, health=5, missing=1, protected=False, color="red"):
        self.scenario_prepare()
        owner = self.player.opponent if opponent else self.player
        target = self.scenario_creature(owner, power=power, health=health, flags=flags or {})
        if current_power is not None:
            target.actual_power = current_power
        if protected:
            self.scenario_buff(target, Indestructible(self.card, target))
        self.player.life = max(1, self.player.ini_life - missing)
        target.color = color
        subaction = 1 if opponent else 11
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_ready(self):
        return self._target_scene(False, {})

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tapped(self):
        return self._target_scene(False, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_flying(self):
        return self._target_scene(False, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._target_scene(False, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_indestructible(self):
        return self._target_scene(False, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_black_color(self):
        return self._target_scene(False, color='black')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_red_color(self):
        return self._target_scene(False, color='red')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_green_color(self):
        return self._target_scene(False, color='green')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_blue_color(self):
        return self._target_scene(False, color='blue')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_white_color(self):
        return self._target_scene(False, color='white')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_gold_color(self):
        return self._target_scene(False, color='gold')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_colorless_color(self):
        return self._target_scene(False, color='colorless')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_ready(self):
        return self._target_scene(True, {})

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tapped(self):
        return self._target_scene(True, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_flying(self):
        return self._target_scene(True, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(True, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_indestructible(self):
        return self._target_scene(True, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_black_color(self):
        return self._target_scene(True, color='black')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_red_color(self):
        return self._target_scene(True, color='red')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_green_color(self):
        return self._target_scene(True, color='green')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_blue_color(self):
        return self._target_scene(True, color='blue')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_white_color(self):
        return self._target_scene(True, color='white')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_gold_color(self):
        return self._target_scene(True, color='gold')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_colorless_color(self):
        return self._target_scene(True, color='colorless')

    @simulate(evidence={'text': ('target.scope', 'exile.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

