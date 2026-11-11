from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Abyssal_Echoes.model import Abyssal_Echoes


@bind_card(Abyssal_Echoes)
class Abyssal_Echoes_Simulation(Card_Simulation):
    scenario_locks={
        '_resource_scene':('opponent.hand', 'opponent.library', 'self.hand', 'self.library'),
    }

    text_parts = {
        "cast.effect": [
            "Randomly cast a creature in your library with total mana value at least {mana_threshold}, without paying its mana cost.",
            "If available, cast a random library creature costing {mana_threshold} or more in total for free.",
            "Choose a creature from your library at random among those with mana value no lower than {mana_threshold}, then cast it freely.",
            "Cast one random available creature in your library with mana value equal to or above {mana_threshold} without paying.",
            "Randomly select and freely cast a library creature whose mana value meets or exceeds {mana_threshold}.",
            "If your library contains eligible creatures with mana value at least {mana_threshold}, randomly cast one at no cost.",
            "Cast for free a random creature from your library whose total mana cost is {mana_threshold} or greater.",
            "Take a random eligible library creature costing at least {mana_threshold} in total and cast it without mana.",
            "Randomly cast one creature from your library with total mana value no less than {mana_threshold}, paying nothing.",
            "Freely cast a creature randomly selected from library creatures costing {mana_threshold} mana or more in total.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _resource_scene(self,count,offset=0,library_count=None,hand_count=None,colored=False):
        library_count=self.scenario_count("library",library_count,reserve=count)
        hand_count=self.scenario_count("hand",hand_count)
        self.scenario_prepare()
        self.player.hand.clear()
        self.player.opponent.hand.clear()
        self.player.library.clear()
        for owner in (self.player, self.player.opponent):
            self.scenario_replace_cards(owner,"library",instant=(library_count, library_count))
            owner.library = [card for card in owner.library if card.type == "Instant"][:library_count]
        self.scenario_clear(self.player,"hand")
        self.scenario_random_cards(self.player,"hand",hand_count)
        subaction = 0
        for index in range(count):
            creature = self.scenario_creature(self.player, power=2, health=3, flags={}, zone="library")
            value = max(0, self.card.effect_params["mana_threshold"] + offset + index)
            creature.mana_cost = "W" * value if colored else str(value)
        return self.scenario_cast()

    @simulate(evidence={'text': ('cast.effect',), 'fields': ('mana_cost',)})
    def simulate_count_0_below(self):
        return self._resource_scene(0,offset=-1)

    @simulate(evidence={'text': ('cast.effect',), 'fields': ('mana_cost',)})
    def simulate_count_0_equal(self):
        return self._resource_scene(0,offset=0)

    @simulate(evidence={'text': ('cast.effect',), 'fields': ('mana_cost',)})
    def simulate_count_0_above(self):
        return self._resource_scene(0,offset=1)

    @simulate(evidence={'text': ('cast.effect',), 'fields': ('mana_cost',)})
    def simulate_count_1_below(self):
        return self._resource_scene(1,offset=-1)

    @simulate(evidence={'text': ('cast.effect',), 'fields': ('mana_cost',)})
    def simulate_count_1_equal(self):
        return self._resource_scene(1,offset=0)

    @simulate(evidence={'text': ('cast.effect',), 'fields': ('mana_cost',)})
    def simulate_count_1_above(self):
        return self._resource_scene(1,offset=1)

    @simulate(evidence={'text': ('cast.effect',), 'fields': ('mana_cost',)})
    def simulate_count_3_below(self):
        return self._resource_scene(3,offset=-1)

    @simulate(evidence={'text': ('cast.effect',), 'fields': ('mana_cost',)})
    def simulate_count_3_equal(self):
        return self._resource_scene(3,offset=0)

    @simulate(evidence={'text': ('cast.effect',), 'fields': ('mana_cost',)})
    def simulate_count_3_above(self):
        return self._resource_scene(3,offset=1)

    @simulate(evidence={'text': ('cast.effect',), 'fields': ('mana_cost',)})
    def simulate_colored_mana_value(self):
        return self._resource_scene(3,colored=True)

