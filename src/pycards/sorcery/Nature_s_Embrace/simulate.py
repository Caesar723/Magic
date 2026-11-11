from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Nature_s_Embrace.model import Nature_s_Embrace


@bind_card(Nature_s_Embrace)
class Nature_s_Embrace_Simulation(Card_Simulation):
    scenario_locks={
        '_recursion_scene':('opponent.battlefield', 'opponent.graveyard', 'opponent.hand', 'self.battlefield', 'self.graveyard', 'self.hand', 'self.library'),
    }

    text_parts = {
        "return.effect": [
            "Put a random creature card from your library into your battlefield, if available.",
            "If there is a creature card from your library, choose one randomly and put it into your battlefield.",
            "Choose a creature card from your library at random and move it into your battlefield, if possible.",
            "Move one random creature card from your library into your battlefield when available.",
            "Randomly select a creature card from your library and put that card into your battlefield, if one exists.",
            "When any creature card from your library is available, choose one at random to move into your battlefield.",
            "Put one available creature card from your library, chosen randomly, into your battlefield.",
            "If possible, take a creature card from your library chosen at random and put it into your battlefield.",
            "Move a randomly chosen creature card from your library into your battlefield if any are available.",
            "Take a random creature card from your library and move it into your battlefield, when one exists.",
        ],
        "return.stats": [
            "Set the returned creature's power and health to {creature_power}/{creature_toughness}.",
            "The returned creature has {creature_power} power and {creature_toughness} health.",
            "Give the returned creature stats of {creature_power}/{creature_toughness}.",
            "Its returned stats are {creature_power} power and {creature_toughness} health.",
            "Make the returned creature a {creature_power}/{creature_toughness}.",
            "The creature enters with {creature_power} power and {creature_toughness} health.",
            "Use {creature_power}/{creature_toughness} as the returned creature's stats.",
            "Assign the returned creature {creature_power} power and {creature_toughness} health.",
            "The returned creature's stats become {creature_power}/{creature_toughness}.",
            "Set its returned power to {creature_power} and health to {creature_toughness}.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _recursion_scene(self, own_count, enemy_count=0, other_count=0, offset=0, colored=False, library_count=None, hand_count=None):
        library_count=self.scenario_count("library",library_count,reserve=own_count)
        hand_count=self.scenario_count("hand",hand_count)
        self.scenario_prepare()
        self.player.graveyard.clear()
        self.player.opponent.graveyard.clear()
        self.player.hand.clear()
        self.player.opponent.hand.clear()
        self.player.library.clear()
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                threshold = self.card.effect_params.get("mana_threshold", 2)
                cost = "W" * (threshold + offset + index + 1) if colored else str(max(0, threshold + offset + index))
                creature = self.scenario_creature(owner, power=index + 2, health=index + 3, flags={}, zone="library" if owner is self.player else "graveyard")
                creature.mana_cost = cost
        self.scenario_cards(self.player,zone="graveyard",instant=other_count,safe=True)
        if library_count is not None:
            self.scenario_cards(self.player,zone="library",instant=library_count)
        self.scenario_random_cards(self.player,"hand",hand_count)
        return self.scenario_cast()

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_none(self):
        return self._recursion_scene(0, 0, 0)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_one_own(self):
        return self._recursion_scene(1, 0, 0)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_one_enemy(self):
        return self._recursion_scene(0, 1, 0)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_both(self):
        return self._recursion_scene(1, 1, 0)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_several(self):
        return self._recursion_scene(3, 3, 0)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_noncreatures(self):
        return self._recursion_scene(0, 0, 3)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_mixed(self):
        return self._recursion_scene(3, 3, 3)

