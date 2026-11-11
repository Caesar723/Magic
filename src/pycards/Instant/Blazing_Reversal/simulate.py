from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Blazing_Reversal.model import Blazing_Reversal


@bind_card(Blazing_Reversal)
class Blazing_Reversal_Simulation(Card_Simulation):
    text_parts = {
        "draw.effect": [
            "Draw 1 card.",
            "Draw one card.",
            "Take the top 1 card of your library into your hand.",
            "Put the top 1 card from your library into your hand.",
            "Add the top 1 card of your library to your hand.",
            "You draw 1 card.",
            "Draw a total of 1 card.",
            "You draw a total of one card.",
            "Take 1 card from the top of your library into your hand.",
            "Put 1 card from the top of your library into your hand.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    def _draw_scene(self, count, with_stack=False):
        self.scenario_prepare({"library": {"instant_number": (count, count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)}})
        self.player.library = [card for card in self.player.library if card.type == "Instant"][:count]
        if with_stack:
            self.scenario_stack()
        return self.scenario_cast(in_stack=with_stack)

    @simulate(evidence={'text': ('draw.effect',), 'fields': ('mana_cost',)})
    def simulate_library_0_no_stack(self):
        return self._draw_scene(0, False)

    @simulate(evidence={'text': ('draw.effect',), 'fields': ('mana_cost',)})
    def simulate_library_0_with_stack(self):
        return self._draw_scene(0, True)

    @simulate(evidence={'text': ('draw.effect',), 'fields': ('mana_cost',)})
    def simulate_library_1_no_stack(self):
        return self._draw_scene(1, False)

    @simulate(evidence={'text': ('draw.effect',), 'fields': ('mana_cost',)})
    def simulate_library_1_with_stack(self):
        return self._draw_scene(1, True)

    @simulate(evidence={'text': ('draw.effect',), 'fields': ('mana_cost',)})
    def simulate_library_3_no_stack(self):
        return self._draw_scene(3, False)

    @simulate(evidence={'text': ('draw.effect',), 'fields': ('mana_cost',)})
    def simulate_library_3_with_stack(self):
        return self._draw_scene(3, True)

