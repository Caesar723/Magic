from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Island.model import Island
from pycards.sorcery.Mindful_Reflection.model import Mindful_Reflection


@bind_card(Mindful_Reflection)
class Mindful_Reflection_Simulation(Card_Simulation):
    scenario_locks={
        '_draw_scene':('opponent.hand', 'opponent.library', 'self.hand', 'self.library'),
    }

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
        "remove.effect": [
            "Then remove up to {discard_count} chosen cards from your hand.",
            "Afterward, choose and remove {discard_count} hand cards, or all of them if fewer exist.",
            "Next, remove up to {discard_count} cards chosen by you from your hand.",
            "You then take up to {discard_count} chosen cards out of your hand.",
            "Following the draw, remove up to {discard_count} selected hand cards.",
            "Then choose and remove up to {discard_count} cards from your hand.",
            "After drawing, take up to {discard_count} hand cards chosen by you out of your hand.",
            "Next, remove {discard_count} chosen cards from your hand if available.",
            "Then remove up to {discard_count} cards selected from your hand.",
            "Afterward, take up to {discard_count} selected cards out of your hand.",
        ],
    }

    def _draw_scene(self,count,hand_count,card_kind="Instant",used=False):
        self.scenario_prepare()
        size=count+hand_count
        if card_kind=="Island":
            pool=[Island(self.player) for _ in range(size)]
        else:
            pool=self.scenario_cards(self.player,**{card_kind.lower():size})
        for card in pool[:count]:
            self.stage_card(card,zone="library")
        for card in pool[count:]:
            self.stage_card(card,zone="hand")
        if used:
            self.card.flag_dict["been used"]=True
        return self.scenario_cast()

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_0_instant(self):
        return self._draw_scene(0, 0, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_1_instant(self):
        return self._draw_scene(0, 1, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_3_instant(self):
        return self._draw_scene(0, 3, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_0_instant(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 0, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_1_instant(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 1, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_3_instant(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 3, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_0_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 0, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_1_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 1, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_3_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 3, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_0_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 0, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_1_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 1, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_3_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 3, 'Instant')

