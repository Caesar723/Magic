from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Eldritch_Rebirth.model import Eldritch_Rebirth


@bind_card(Eldritch_Rebirth)
class Eldritch_Rebirth_Simulation(Card_Simulation):
    scenario_locks={
        '_recursion_scene':('opponent.graveyard', 'opponent.hand', 'self.graveyard', 'self.hand', 'self.library'),
    }

    text_parts = {
        "return.effect": [
            "Return every creature in your graveyard with total mana value at most {mana_threshold} to your battlefield.",
            "Put all creatures from your graveyard with mana value {mana_threshold} or less onto your battlefield.",
            "Move each graveyard creature whose total mana cost does not exceed {mana_threshold} onto your battlefield.",
            "Every creature in your graveyard with mana value no greater than {mana_threshold} returns to your battlefield.",
            "Return all graveyard creatures whose mana value is at most {mana_threshold} to your battlefield.",
            "Take each creature from your graveyard with total mana cost of {mana_threshold} or less and put it into play.",
            "All creatures in your graveyard with mana value equal to or below {mana_threshold} return to your battlefield.",
            "Move every graveyard creature with total mana value no higher than {mana_threshold} into play under your control.",
            "Return your graveyard creatures to your battlefield if their total mana value is {mana_threshold} or less.",
            "Put each creature in your graveyard with mana value at most {mana_threshold} into play on your side.",
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

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_none(self):
        return self._recursion_scene(0, 0, 0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_one_own(self):
        return self._recursion_scene(1, 0, 0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_one_enemy(self):
        return self._recursion_scene(0, 1, 0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_both(self):
        return self._recursion_scene(1, 1, 0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_several(self):
        return self._recursion_scene(3, 3, 0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_noncreatures(self):
        return self._recursion_scene(0, 0, 3)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_mixed(self):
        return self._recursion_scene(3, 3, 3)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_cost_below(self):
        return self._recursion_scene(1, offset=-1)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_cost_equal(self):
        return self._recursion_scene(1, offset=0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_cost_above(self):
        return self._recursion_scene(1, offset=1)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_colored_cost(self):
        return self._recursion_scene(2, colored=True)

