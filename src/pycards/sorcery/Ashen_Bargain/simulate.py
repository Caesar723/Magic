from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Ashen_Bargain.model import Ashen_Bargain


@bind_card(Ashen_Bargain)
class Ashen_Bargain_Simulation(Card_Simulation):
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
        "loss.effect": [
            "Then you lose {life_loss} life.",
            "Afterward, lose {life_loss} life.",
            "You then lose {life_loss} life.",
            "Next, reduce your life total by {life_loss}.",
            "Then reduce your life total by {life_loss}.",
            "After drawing, you lose {life_loss} life.",
            "Following the draw, lose {life_loss} life.",
            "Next, you lose {life_loss} life.",
            "Afterward, your life total decreases by {life_loss}.",
            "The draw is followed by you losing {life_loss} life.",
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

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_empty_life_below(self):
        return self._draw_scene(0, self.card.effect_params["life_loss"] - 1)

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_empty_life_equal(self):
        return self._draw_scene(0, self.card.effect_params["life_loss"])

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_empty_life_above(self):
        return self._draw_scene(0, self.card.effect_params["life_loss"] + 1)

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_short_life_below(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), self.card.effect_params["life_loss"] - 1)

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_short_life_equal(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), self.card.effect_params["life_loss"])

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_short_life_above(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), self.card.effect_params["life_loss"] + 1)

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_exact_life_below(self):
        return self._draw_scene(self.card.effect_params["draw_count"], self.card.effect_params["life_loss"] - 1)

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_exact_life_equal(self):
        return self._draw_scene(self.card.effect_params["draw_count"], self.card.effect_params["life_loss"])

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_exact_life_above(self):
        return self._draw_scene(self.card.effect_params["draw_count"], self.card.effect_params["life_loss"] + 1)

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_plenty_life_below(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + 2, self.card.effect_params["life_loss"] - 1)

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_plenty_life_equal(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + 2, self.card.effect_params["life_loss"])

    @simulate(evidence={'text': ('draw.effect', 'loss.effect'), 'fields': ('mana_cost',)})
    def simulate_draw_plenty_life_above(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + 2, self.card.effect_params["life_loss"] + 1)

