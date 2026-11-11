from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Island.model import Island
from pycards.Instant.Ephemeral_Insight.model import Ephemeral_Insight


@bind_card(Ephemeral_Insight)
class Ephemeral_Insight_Simulation(Card_Simulation):
    scenario_locks={
        '_draw_scene':('opponent.hand', 'opponent.library', 'self.hand', 'self.library'),
    }

    text_parts = {
        "scry.effect": [
            "Look at up to the top {scry_count} cards of your library, keep any of them on top in their existing order, and move the rest to the bottom in their existing order.",
            "Examine the top {scry_count} cards of your library or fewer if necessary, keep any on top in order, and put the others on the bottom in order.",
            "Inspect up to {scry_count} cards from the top of your library, leaving chosen cards on top and moving the unchosen cards to the bottom without reordering either group.",
            "Look at the first {scry_count} available library cards, choose which to keep on top, and put the rest on the bottom while preserving each group's order.",
            "Examine up to the first {scry_count} cards of your library, retaining any on top and moving the others to the bottom in their current order.",
            "Look through up to the top {scry_count} library cards, leave any chosen cards on top in order, and place the remaining cards at the bottom in order.",
            "Inspect the top {scry_count} cards of your library or all of it if smaller, keep any on top, and move the rest to the bottom without changing their relative order.",
            "View up to {scry_count} cards from the top of your library, keep your chosen cards there, and place the rest at the bottom while maintaining both groups' order.",
            "Examine at most the top {scry_count} library cards, retaining any chosen cards in place and moving all remaining examined cards to the bottom in order.",
            "Look at up to {scry_count} cards from the top, keep any of them there in their current order, and put the remaining examined cards at the bottom in their current order.",
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
        "copy.effect": [
            "If this is its first use, add a copy of this card to your hand, marked as already used.",
            "On its first use only, put a copy of this card into your hand and mark the copy as used.",
            "If this card has not been used before, create a copy in your hand with its used flag set.",
            "If this card is not already marked used, add a copy to your hand marked used.",
            "Only if this card has not previously been used, put an already-used copy into your hand.",
            "If this is an unused card, add a copy to your hand and mark that copy as used.",
            "When this card is used for the first time, add a copy marked used to your hand.",
            "If it has not already been used, put a used copy of this card into your hand.",
            "If this card was unused, create a copy in your hand that is marked as used.",
            "Only on the first use of this card, add an already-used copy of it to your hand.",
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

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_0_instant(self):
        return self._draw_scene(0, 0, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_1_instant(self):
        return self._draw_scene(0, 1, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_3_instant(self):
        return self._draw_scene(0, 3, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_0_instant(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 0, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_1_instant(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 1, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_3_instant(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 3, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_0_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 0, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_1_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 1, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_3_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 3, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_0_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 0, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_1_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 1, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_3_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 3, 'Instant')

    @simulate(evidence={'text': ('scry.effect', 'draw.effect', 'copy.effect'), 'fields': ('mana_cost',)})
    def simulate_already_used_copy(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + 3, 1, used=True)

