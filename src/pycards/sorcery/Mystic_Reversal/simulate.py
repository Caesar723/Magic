from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Island.model import Island
from pycards.sorcery.Mystic_Reversal.model import Mystic_Reversal


@bind_card(Mystic_Reversal)
class Mystic_Reversal_Simulation(Card_Simulation):
    text_parts = {
        "draw.effect": [
            "You and your opponent each draw {draw_count} card{draw_count_plural}.",
            "Both players draw {draw_count} card{draw_count_plural} each.",
            "Each player draws {draw_count} card{draw_count_plural}.",
            "You draw {draw_count} card{draw_count_plural}, then your opponent does the same.",
            "Both you and your opponent draw {draw_count_word} card{draw_count_plural}.",
            "Every player draws {draw_count} card{draw_count_plural}.",
            "Have each player draw {draw_count} card{draw_count_plural}.",
            "Have both players draw {draw_count_word} card{draw_count_plural} each.",
            "You draw {draw_count_word} card{draw_count_plural}, followed by your opponent drawing the same number.",
            "Each of the two players draws {draw_count_word} card{draw_count_plural}.",
        ],
        "remove.effect": [
            "Then remove up to {discard_count} random cards from each player's hand.",
            "Afterward, randomly remove {discard_count} hand cards, or all of them if fewer exist.",
            "Next, remove up to {discard_count} cards chosen at random from each player's hand.",
            "Both players then take up to {discard_count} random cards out of each player's hand.",
            "Following the draw, remove up to {discard_count} randomly selected hand cards.",
            "Then randomly choose and remove up to {discard_count} cards from each player's hand.",
            "After drawing, each player takes up to {discard_count} hand cards chosen at random out of each player's hand.",
            "Next, remove {discard_count} randomly chosen cards from each player's hand if available.",
            "Then remove up to {discard_count} cards randomly selected from each player's hand.",
            "Afterward, take up to {discard_count} randomly selected cards out of each player's hand.",
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

    def _both_scene(self, own_count, enemy_count, hand_count):
        record = self._draw_scene(own_count, hand_count)
        size = enemy_count + hand_count
        self.room.env_initinal_library(self.player.opponent, {"instant_number": (size, size), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)})
        pool = [card for card in self.player.opponent.library if card.type == "Instant"]
        self.player.opponent.library = pool[:enemy_count]
        self.player.opponent.hand = pool[enemy_count:]
        return record

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_empty_enemy_empty_hand_0(self):
        return self._both_scene(0, 0, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_empty_enemy_empty_hand_3(self):
        return self._both_scene(0, 0, 3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_empty_enemy_exact_hand_0(self):
        return self._both_scene(0, self.card.effect_params["draw_count"], 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_empty_enemy_exact_hand_3(self):
        return self._both_scene(0, self.card.effect_params["draw_count"], 3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_empty_enemy_plenty_hand_0(self):
        return self._both_scene(0, self.card.effect_params["draw_count"] + 2, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_empty_enemy_plenty_hand_3(self):
        return self._both_scene(0, self.card.effect_params["draw_count"] + 2, 3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_exact_enemy_empty_hand_0(self):
        return self._both_scene(self.card.effect_params["draw_count"], 0, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_exact_enemy_empty_hand_3(self):
        return self._both_scene(self.card.effect_params["draw_count"], 0, 3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_exact_enemy_exact_hand_0(self):
        return self._both_scene(self.card.effect_params["draw_count"], self.card.effect_params["draw_count"], 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_exact_enemy_exact_hand_3(self):
        return self._both_scene(self.card.effect_params["draw_count"], self.card.effect_params["draw_count"], 3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_exact_enemy_plenty_hand_0(self):
        return self._both_scene(self.card.effect_params["draw_count"], self.card.effect_params["draw_count"] + 2, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_exact_enemy_plenty_hand_3(self):
        return self._both_scene(self.card.effect_params["draw_count"], self.card.effect_params["draw_count"] + 2, 3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_plenty_enemy_empty_hand_0(self):
        return self._both_scene(self.card.effect_params["draw_count"] + 2, 0, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_plenty_enemy_empty_hand_3(self):
        return self._both_scene(self.card.effect_params["draw_count"] + 2, 0, 3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_plenty_enemy_exact_hand_0(self):
        return self._both_scene(self.card.effect_params["draw_count"] + 2, self.card.effect_params["draw_count"], 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_plenty_enemy_exact_hand_3(self):
        return self._both_scene(self.card.effect_params["draw_count"] + 2, self.card.effect_params["draw_count"], 3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_plenty_enemy_plenty_hand_0(self):
        return self._both_scene(self.card.effect_params["draw_count"] + 2, self.card.effect_params["draw_count"] + 2, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_both_self_plenty_enemy_plenty_hand_3(self):
        return self._both_scene(self.card.effect_params["draw_count"] + 2, self.card.effect_params["draw_count"] + 2, 3)

