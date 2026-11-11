from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.Instant.Time_Warp.model import Time_Warp


@bind_card(Time_Warp)
class Time_Warp_Simulation(Card_Simulation):
    text_parts = {
        "turn.effect": [
            "Take {extra_turns} extra turn{extra_turns_plural} after this turn.",
            "After this turn, take {extra_turns} additional turn{extra_turns_plural}.",
            "You get {extra_turns} extra turn{extra_turns_plural} following this one.",
            "Add {extra_turns} extra turn{extra_turns_plural} for yourself after the current turn.",
            "Take {extra_turns_article_an} extra turn{extra_turns_plural} following the current one.",
            "You take {extra_turns} additional turn{extra_turns_plural} after this one ends.",
            "The current turn is followed by {extra_turns} extra turn{extra_turns_plural} for you.",
            "Give yourself {extra_turns} extra turn{extra_turns_plural} after this turn.",
            "You gain {extra_turns} extra turn{extra_turns_plural} to take after this one.",
            "Queue {extra_turns} additional turn{extra_turns_plural} for yourself after the current turn.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _turn_scene(self, queued, lands=0):
        self.scenario_prepare()
        self.player.counter_dict["extra_turn"] = queued
        for _ in range(lands):
            land = Plains(self.player)
            land.tap()
            self.stage_card(land, zone="land_area")
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('turn.effect',), 'fields': ('mana_cost',)})
    def simulate_queued_0_tapped_0(self):
        return self._turn_scene(0, 0)

    @simulate(evidence={'text': ('turn.effect',), 'fields': ('mana_cost',)})
    def simulate_queued_0_tapped_3(self):
        return self._turn_scene(0, 3)

    @simulate(evidence={'text': ('turn.effect',), 'fields': ('mana_cost',)})
    def simulate_queued_1_tapped_0(self):
        return self._turn_scene(1, 0)

    @simulate(evidence={'text': ('turn.effect',), 'fields': ('mana_cost',)})
    def simulate_queued_1_tapped_3(self):
        return self._turn_scene(1, 3)

    @simulate(evidence={'text': ('turn.effect',), 'fields': ('mana_cost',)})
    def simulate_queued_3_tapped_0(self):
        return self._turn_scene(3, 0)

    @simulate(evidence={'text': ('turn.effect',), 'fields': ('mana_cost',)})
    def simulate_queued_3_tapped_3(self):
        return self._turn_scene(3, 3)

