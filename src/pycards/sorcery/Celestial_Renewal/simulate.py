from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Celestial_Renewal.model import Celestial_Renewal


@bind_card(Celestial_Renewal)
class Celestial_Renewal_Simulation(Card_Simulation):
    scenario_locks={
        '_recursion_scene':('opponent.graveyard', 'opponent.hand', 'self.graveyard', 'self.hand', 'self.library'),
    }

    text_parts = {
        "return.effect": [
            "If your graveyard contains at least two creatures, return two random ones to your battlefield.",
            "With at least two creature cards in your graveyard, put two selected randomly onto your battlefield.",
            "Return two randomly selected creatures from your graveyard to your battlefield only if at least two are available.",
            "If two or more graveyard creatures are available, move two at random onto your battlefield.",
            "When your graveyard has at least two creature cards, choose two randomly to return to your battlefield.",
            "Put two random creature cards from your graveyard into play, provided at least two exist there.",
            "If you have two or more creatures in your graveyard, return two chosen randomly to your battlefield.",
            "Return a random pair of creatures from your graveyard to your battlefield if a pair is available.",
            "Choose two creatures from your graveyard at random and return them to your battlefield if there are at least two.",
            "Only when two or more creatures are in your graveyard, put a random two of them onto your battlefield.",
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

