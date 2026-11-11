from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Island.model import Island
from pycards.sorcery.Mind_s_Insight.model import Mind_s_Insight


@bind_card(Mind_s_Insight)
class Mind_s_Insight_Simulation(Card_Simulation):
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
        "remove.selection": [
            "Then choose a random card in your hand, if any.",
            "Afterward, select a random hand card if available.",
            "Next, pick a card at random from your hand if it is nonempty.",
            "Then, if your hand contains a card, randomly choose one.",
            "After drawing, choose one random hand card if possible.",
            "Following the draw, randomly select one card in your hand, if any.",
            "Then randomly pick one card from your hand if one is present.",
            "Next, choose one of your hand cards at random if any remain.",
            "Afterward, randomly choose a card from your hand if there is one.",
            "Then pick one randomly selected card in your hand, if possible.",
        ],
        "remove.condition": [
            "Remove the selected card from your hand unless its type label is contained in the text \"Island\".",
            "Keep that card only if its type label occurs within \"Island\", and otherwise remove it from your hand.",
            "Take that card out of your hand if its type label is not a substring of \"Island\".",
            "If \"Island\" does not contain the chosen card's type label, remove that card from your hand.",
            "Leave the chosen card in hand if its type label is contained in \"Island\". Otherwise, remove it.",
            "Remove that hand card unless the text \"Island\" includes its type label.",
            "If its type label does not occur in \"Island\", take the selected card out of your hand.",
            "Keep the selected card when its type label is a substring of \"Island\", removing it otherwise.",
            "Only a selected card whose type label occurs within \"Island\" remains in hand. Remove any other selected card.",
            "If the selected card's type label is not contained within \"Island\", remove the card from your hand.",
        ],
    }

    def _draw_scene(self, count, hand_count, card_kind="Instant", used=False):
        size = count + hand_count + 1
        self.scenario_prepare({"library": {"instant_number": (size, size), "sorcery_number": (size, size), "creature_number": (size, size), "land_number": (0, 0)}})
        pool = [card for card in self.player.library if card.type == card_kind]
        if card_kind == "Island":
            pool = [Island(self.player) for _ in range(size)]
        self.player.library = pool[:count]
        self.player.hand = pool[count:count + hand_count + 1] if hand_count else []
        if used:
            self.card.flag_dict["been used"] = True
        return self.scenario_cast()

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_empty_library(self):
        self.scenario_prepare()
        self.player.hand.clear()
        self.player.library.clear()
        return self.scenario_cast()

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_1_instant(self):
        return self._draw_scene(0, 1, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_1_sorcery(self):
        return self._draw_scene(0, 1, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_1_creature(self):
        return self._draw_scene(0, 1, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_1_island(self):
        return self._draw_scene(0, 1, 'Island')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_3_instant(self):
        return self._draw_scene(0, 3, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_3_sorcery(self):
        return self._draw_scene(0, 3, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_3_creature(self):
        return self._draw_scene(0, 3, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_empty_hand_3_island(self):
        return self._draw_scene(0, 3, 'Island')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_0_instant(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 0, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_0_sorcery(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 0, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_0_creature(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 0, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_0_island(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 0, 'Island')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_1_instant(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 1, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_1_sorcery(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 1, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_1_creature(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 1, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_1_island(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 1, 'Island')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_3_instant(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 3, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_3_sorcery(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 3, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_3_creature(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 3, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_short_draw_hand_3_island(self):
        return self._draw_scene(max(0, self.card.effect_params["draw_count"] - 1), 3, 'Island')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_0_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 0, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_0_sorcery(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 0, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_0_creature(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 0, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_0_island(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 0, 'Island')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_1_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 1, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_1_sorcery(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 1, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_1_creature(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 1, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_1_island(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 1, 'Island')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_3_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 3, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_3_sorcery(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 3, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_3_creature(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 3, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_exact_draw_hand_3_island(self):
        return self._draw_scene(self.card.effect_params["draw_count"], 3, 'Island')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_0_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 0, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_0_sorcery(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 0, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_0_creature(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 0, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_0_island(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 0, 'Island')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_1_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 1, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_1_sorcery(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 1, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_1_creature(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 1, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_1_island(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 1, 'Island')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_3_instant(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 3, 'Instant')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_3_sorcery(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 3, 'Sorcery')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_3_creature(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 3, 'Creature')

    @simulate(evidence={'text': ('draw.effect', 'remove.selection', 'remove.condition'), 'fields': ('mana_cost',)})
    def simulate_plenty_hand_3_island(self):
        return self._draw_scene(self.card.effect_params["draw_count"] + self.card.effect_params.get("scry_count", 0) + 3, 3, 'Island')

