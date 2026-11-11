from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.Instant.Shadowstrike.model import Shadowstrike


@bind_card(Shadowstrike)
class Shadowstrike_Simulation(Card_Simulation):
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
        "destroy.condition": [
            "If the target is tapped,",
            "If that creature is tapped,",
            "When the chosen creature is tapped,",
            "If the selected creature is tapped,",
            "If you chose a tapped creature,",
            "When your target is tapped,",
            "If the targeted creature is tapped,",
            "If the chosen target is tapped,",
            "When that creature is tapped,",
            "If you selected a creature that is already tapped,",
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
        "draw.effect": [
            "Draw {draw_count} card{draw_count_plural}.",
            "Draw {draw_count_word} card{draw_count_plural}.",
            "Take the top {draw_count} card{draw_count_plural} of your library into your hand.",
            "Put the top {draw_count} card{draw_count_plural} from your library into your hand.",
            "Add the top {draw_count} card{draw_count_plural} of your library to your hand.",
            "You draw {draw_count} card{draw_count_plural}.",
            "Draw a total of {draw_count} card{draw_count_plural}.",
            "You draw a total of {draw_count_word} card{draw_count_plural}.",
            "Take {draw_count} card{draw_count_plural} from the top of your library into your hand.",
            "Put {draw_count} card{draw_count_plural} from the top of your library into your hand.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _target_scene(self, opponent, flags=None, power=3, current_power=None, health=5, missing=1, protected=False, library_count=None):
        self.scenario_prepare()
        owner = self.player.opponent if opponent else self.player
        target = self.scenario_creature(owner, power=power, health=health, flags=flags or {})
        if current_power is not None:
            target.actual_power = current_power
        if protected:
            target.gain_buff(Indestructible(self.card, target), self.card)
        self.player.life = max(1, self.player.ini_life - missing)
        if library_count is not None:
            self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "creature_number": (0, 0), "sorcery_number": (0, 0), "land_number": (0, 0)})
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        subaction = 1 if opponent else 11
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_ready(self):
        return self._target_scene(False, {})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tapped(self):
        return self._target_scene(False, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_flying(self):
        return self._target_scene(False, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._target_scene(False, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_indestructible(self):
        return self._target_scene(False, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_draw_empty(self):
        return self._target_scene(False, library_count=0)

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_draw_short(self):
        return self._target_scene(False, library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_draw_exact(self):
        return self._target_scene(False, library_count=self.card.effect_params["draw_count"])

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_ready(self):
        return self._target_scene(True, {})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tapped(self):
        return self._target_scene(True, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_flying(self):
        return self._target_scene(True, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(True, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_indestructible(self):
        return self._target_scene(True, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_draw_empty(self):
        return self._target_scene(True, library_count=0)

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_draw_short(self):
        return self._target_scene(True, library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_draw_exact(self):
        return self._target_scene(True, library_count=self.card.effect_params["draw_count"])

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

