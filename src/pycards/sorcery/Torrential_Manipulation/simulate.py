from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Torrential_Manipulation.model import Torrential_Manipulation


@bind_card(Torrential_Manipulation)
class Torrential_Manipulation_Simulation(Card_Simulation):
    text_parts = {
        "return.effect": [
            "Return the selected creature to its owner's hand. Choose only an opposing creature.",
            "Put the target creature into its owner's hand. Choose only an opposing creature.",
            "The chosen creature returns to its owner's hand. Choose only an opposing creature.",
            "Move that creature from the battlefield to its owner's hand. Choose only an opposing creature.",
            "Return the creature you targeted to the hand of its owner. Choose only an opposing creature.",
            "Put that creature back into its owner's hand. Choose only an opposing creature.",
            "The targeted creature goes back to its owner's hand. Choose only an opposing creature.",
            "Return your chosen creature from play to its owner's hand. Choose only an opposing creature.",
            "Take that creature off the battlefield and put it into its owner's hand. Choose only an opposing creature.",
            "Move the targeted creature back to its owner's hand. Choose only an opposing creature.",
        ],
        "cast.effect": [
            "Then cast a random non-counter instant or sorcery from your opponent's hand without paying its cost, if available.",
            "If available, randomly cast one opposing hand instant or sorcery other than a counterspell for free.",
            "Choose a non-counter instant or sorcery from your opponent's hand at random and cast it without cost, if possible.",
            "Randomly cast one available non-counter instant or sorcery in the opposing hand without paying.",
            "Afterward, cast for free a random instant or sorcery in your opponent's hand, excluding counterspells.",
            "If the opposing hand has any eligible non-counter instant or sorcery, randomly cast one for free.",
            "Cast one random non-counter instant or sorcery from the opposing hand at no mana cost, when available.",
            "Then randomly select an opposing hand instant or sorcery that is not a counterspell and cast it freely.",
            "Take a random available non-counter instant or sorcery from your opponent's hand and cast it without paying mana.",
            "If possible, freely cast an instant or sorcery chosen randomly from your opponent's hand, excluding counters.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _resource_scene(self, count, offset=0, role="enemy", library_count=3, hand_count=2, colored=False):
        self.scenario_prepare()
        self.player.hand.clear()
        self.player.opponent.hand.clear()
        self.player.library.clear()
        for owner in (self.player, self.player.opponent):
            self.room.env_initinal_library(owner, {"instant_number": (library_count, library_count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)})
            owner.library = [card for card in owner.library if card.type == "Instant"][:library_count]
        self.room.env_initinal_hand(self.player.opponent, {"instant_number": (hand_count, hand_count), "sorcery_number": (hand_count, hand_count), "creature_number": (0, 0), "land_number": (0, 0)})
        subaction = 0
        if count:
            owner = self.player if role == "self" else self.player.opponent
            self.scenario_creature(owner, power=2, health=4, flags={}, mana_cost=str(max(0, 2 + offset)))
            subaction = 11 if owner is self.player else 1
        hand_owner = self.player.opponent
        for index, card in enumerate(hand_owner.hand):
            card.mana_cost = str(max(0, 2 + offset + index - 1))
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_0_below(self):
        return self._resource_scene(0, offset=-1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_0_equal(self):
        return self._resource_scene(0, offset=0)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_0_above(self):
        return self._resource_scene(0, offset=1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_1_below(self):
        return self._resource_scene(1, offset=-1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_1_equal(self):
        return self._resource_scene(1, offset=0)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_1_above(self):
        return self._resource_scene(1, offset=1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_3_below(self):
        return self._resource_scene(3, offset=-1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_3_equal(self):
        return self._resource_scene(3, offset=0)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_3_above(self):
        return self._resource_scene(3, offset=1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_self_target(self):
        return self._resource_scene(1, role="self")

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_no_followup_spell(self):
        return self._resource_scene(1, hand_count=0)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_zero_cost_target(self):
        return self._resource_scene(1, offset=-2)

