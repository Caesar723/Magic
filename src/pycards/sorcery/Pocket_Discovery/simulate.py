from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Pocket_Discovery.model import Pocket_Discovery


@bind_card(Pocket_Discovery)
class Pocket_Discovery_Simulation(Card_Simulation):
    text_parts = {
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

    def _draw_scene(self, library_count, life=None):
        self.scenario_prepare({"library": {"instant_number": (library_count, library_count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)}})
        self.player.library = self.player.library[:library_count]
        if life is not None:
            if not 1 <= life <= self.player.ini_life:
                return self.scenario_skip()
            self.player.life = life
        return self.scenario_cast()

    @simulate(evidence={'text': ('draw.effect',), 'fields': ('mana_cost',)})
    def simulate_draw_empty_life_normal(self):
        return self._draw_scene(0, None)

    @simulate(evidence={'text': ('draw.effect',), 'fields': ('mana_cost',)})
    def simulate_draw_short_life_normal(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), None)

    @simulate(evidence={'text': ('draw.effect',), 'fields': ('mana_cost',)})
    def simulate_draw_exact_life_normal(self):
        return self._draw_scene(self.card.effect_params["draw_count"], None)

    @simulate(evidence={'text': ('draw.effect',), 'fields': ('mana_cost',)})
    def simulate_draw_plenty_life_normal(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + 2, None)

