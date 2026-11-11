from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Time_Warp.model import Time_Warp


@bind_card(Time_Warp)
class Time_Warp_Simulation(Card_Simulation):
    scenario_locks={
        '_recursion_scene':('opponent.graveyard', 'opponent.hand', 'self.graveyard', 'self.hand', 'self.library'),
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
            "Then randomly remove {discard_count} cards from your hand, or all if fewer remain.",
            "Next, remove {discard_count} randomly chosen hand cards, limited by availability.",
            "Randomly choose and remove up to {discard_count} cards from your hand, taking all if fewer.",
            "Afterward, remove {discard_count} random cards from your hand if available.",
            "Take {discard_count} random cards out of your hand, or as many as remain.",
            "Remove cards randomly from your hand {discard_count} times while any are available.",
            "Then remove as many as {discard_count} available cards randomly from your hand.",
            "Remove up to {discard_count} randomly selected hand cards, taking all available if fewer.",
            "Next, randomly take {discard_count} cards out of your hand, stopping if empty.",
            "After drawing, remove {discard_count} random hand cards, or all if there are fewer.",
        ],
        "return.effect": [
            "Put a random card from your graveyard, including this spell into the top of your library, if available.",
            "If there is a card from your graveyard, including this spell, choose one randomly and put it into the top of your library.",
            "Choose a card from your graveyard, including this spell at random and move it into the top of your library, if possible.",
            "Move one random card from your graveyard, including this spell into the top of your library when available.",
            "Randomly select a card from your graveyard, including this spell and put that card into the top of your library, if one exists.",
            "When any card from your graveyard, including this spell is available, choose one at random to move into the top of your library.",
            "Put one available card from your graveyard, including this spell, chosen randomly, into the top of your library.",
            "If possible, take a card from your graveyard, including this spell chosen at random and put it into the top of your library.",
            "Move a randomly chosen card from your graveyard, including this spell into the top of your library if any are available.",
            "Take a random card from your graveyard, including this spell and move it into the top of your library, when one exists.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _recursion_scene(self, own_count, enemy_count=0, other_count=0, offset=0, colored=False, library_count=None, hand_count=None):
        library_count=self.scenario_count("library",library_count)
        hand_count=self.scenario_count("hand",hand_count)
        self.scenario_prepare()
        self.player.graveyard.clear()
        self.player.opponent.graveyard.clear()
        self.player.hand.clear()
        self.player.opponent.hand.clear()
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                threshold = self.card.effect_params.get("mana_threshold", 2)
                cost = "W" * (threshold + offset + index + 1) if colored else str(max(0, threshold + offset + index))
                creature = self.scenario_creature(owner, power=index + 2, health=index + 3, flags={}, zone="graveyard")
                creature.mana_cost = cost
        self.scenario_cards(self.player,zone="graveyard",instant=other_count,safe=True)
        if library_count is not None:
            self.scenario_replace_cards(self.player,"library",instant=(library_count, library_count))
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        self.scenario_random_cards(self.player,"hand",hand_count)
        return self.scenario_cast()

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_graves_none(self):
        return self._recursion_scene(0, 0, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_graves_one_own(self):
        return self._recursion_scene(1, 0, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_graves_one_enemy(self):
        return self._recursion_scene(0, 1, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_graves_both(self):
        return self._recursion_scene(1, 1, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_graves_several(self):
        return self._recursion_scene(3, 3, 0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_graves_noncreatures(self):
        return self._recursion_scene(0, 0, 3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_graves_mixed(self):
        return self._recursion_scene(3, 3, 3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty_hand_0(self):
        return self._recursion_scene(0, other_count=3, library_count=0, hand_count=0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty_hand_1(self):
        return self._recursion_scene(0, other_count=3, library_count=0, hand_count=1)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty_hand_3(self):
        return self._recursion_scene(0, other_count=3, library_count=0, hand_count=3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short_hand_0(self):
        return self._recursion_scene(0, other_count=3, library_count=max(0, self.card.effect_params["draw_count"] - 1), hand_count=0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short_hand_1(self):
        return self._recursion_scene(0, other_count=3, library_count=max(0, self.card.effect_params["draw_count"] - 1), hand_count=1)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short_hand_3(self):
        return self._recursion_scene(0, other_count=3, library_count=max(0, self.card.effect_params["draw_count"] - 1), hand_count=3)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact_hand_0(self):
        return self._recursion_scene(0, other_count=3, library_count=self.card.effect_params["draw_count"], hand_count=0)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact_hand_1(self):
        return self._recursion_scene(0, other_count=3, library_count=self.card.effect_params["draw_count"], hand_count=1)

    @simulate(evidence={'text': ('draw.effect', 'remove.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact_hand_3(self):
        return self._recursion_scene(0, other_count=3, library_count=self.card.effect_params["draw_count"], hand_count=3)

