from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Ethereal_Reversal.model import Ethereal_Reversal


@bind_card(Ethereal_Reversal)
class Ethereal_Reversal_Simulation(Card_Simulation):
    scenario_locks={
        '_resource_scene':('opponent.battlefield', 'opponent.hand', 'opponent.library', 'self.battlefield', 'self.hand', 'self.library'),
    }

    text_parts = {
        "return.effect": [
            "Return the selected creature to its owner's hand.",
            "Put the target creature into its owner's hand.",
            "The chosen creature returns to its owner's hand.",
            "Move that creature from the battlefield to its owner's hand.",
            "Return the creature you targeted to the hand of its owner.",
            "Put that creature back into its owner's hand.",
            "The targeted creature goes back to its owner's hand.",
            "Return your chosen creature from play to its owner's hand.",
            "Take that creature off the battlefield and put it into its owner's hand.",
            "Move the targeted creature back to its owner's hand.",
        ],
        "cast.effect": [
            "If the returned creature had positive mana value, cast the first instant or sorcery in your hand costing no more than that value, without paying its cost.",
            "When the returned creature's mana value is positive, cast the earliest hand instant or sorcery with mana value no greater than it for free.",
            "If its mana value exceeds zero, freely cast the first instant or sorcery in hand whose mana value does not exceed that creature's.",
            "After returning a creature with positive mana value, cast your first eligible hand instant or sorcery of at most that mana value without cost.",
            "For a returned creature with mana value above zero, cast the first hand instant or sorcery costing that much or less for free.",
            "If a positive-mana-value creature was returned, freely cast the first qualifying instant or sorcery in your hand costing no more than it.",
            "When the returned creature costs more than zero, cast your earliest hand instant or sorcery with no greater mana value, paying nothing.",
            "If the returned creature has positive total mana cost, cast the first hand instant or sorcery whose total cost is at most that value for free.",
            "Cast your first eligible hand instant or sorcery for free if its mana value is no greater than the returned creature's positive mana value.",
            "If that creature's mana value was positive, take the first instant or sorcery in hand costing no more and cast it without paying.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _resource_scene(self,count,offset=0,role='enemy',library_count=None,hand_count=None):
        library_count=self.scenario_count("library",library_count)
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
        if count:
            owner = self.player if role == "self" else self.player.opponent
            self.scenario_creature(owner, power=2, health=4, flags={}, mana_cost=str(max(0, 2 + offset)))
            subaction = 11 if owner is self.player else 1
        hand_owner = self.player
        for index, card in enumerate(hand_owner.hand):
            card.mana_cost = str(max(0, 2 + offset + index - 1))
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_0_below(self):
        return self._resource_scene(0,offset=-1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_0_equal(self):
        return self._resource_scene(0,offset=0)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_0_above(self):
        return self._resource_scene(0,offset=1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_1_below(self):
        return self._resource_scene(1,offset=-1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_1_equal(self):
        return self._resource_scene(1,offset=0)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_1_above(self):
        return self._resource_scene(1,offset=1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_3_below(self):
        return self._resource_scene(3,offset=-1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_3_equal(self):
        return self._resource_scene(3,offset=0)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_count_3_above(self):
        return self._resource_scene(3,offset=1)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_self_target(self):
        return self._resource_scene(1,role="self")

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_no_followup_spell(self):
        return self._resource_scene(1,hand_count=0)

    @simulate(evidence={'text': ('return.effect', 'cast.effect'), 'fields': ('mana_cost',)})
    def simulate_zero_cost_target(self):
        return self._resource_scene(1,offset=-2)

