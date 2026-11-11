from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Time_Rift_Convergence.model import Time_Rift_Convergence


@bind_card(Time_Rift_Convergence)
class Time_Rift_Convergence_Simulation(Card_Simulation):
    scenario_locks={
        '_recursion_scene':('opponent.graveyard', 'opponent.hand', 'self.graveyard', 'self.hand', 'self.library'),
    }

    text_parts = {
        "return.effect": [
            "Return exactly {return_count} random cards from your graveyard to your hand, possibly including this spell.",
            "Choose {return_count} graveyard cards randomly and return them to your hand, with this spell eligible.",
            "Move {return_count} random cards from your graveyard into your hand, allowing this spell among them.",
            "Take exactly {return_count} cards from your graveyard at random into your hand, including this spell as a candidate.",
            "Return a random set of {return_count} graveyard cards to your hand, possibly selecting this spell.",
            "Put {return_count} cards chosen randomly from your graveyard into your hand, with this spell eligible too.",
            "Randomly sample {return_count} cards from your graveyard and move them into your hand, allowing this spell.",
            "Bring exactly {return_count} random graveyard cards into your hand, possibly this spell itself.",
            "Return {return_count} randomly chosen cards from your graveyard to your hand, including this spell in the pool.",
            "Move a random {return_count} cards from your graveyard to your hand, with this spell among the possible choices.",
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
        if len(self.player.graveyard) + 1 < self.card.effect_params["return_count"]:
            return self.scenario_skip()
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
    def simulate_return_count_short(self):
        return self._recursion_scene(0, other_count=max(0, self.card.effect_params["return_count"] - 2))

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_return_count_exact(self):
        return self._recursion_scene(0, other_count=max(0, self.card.effect_params["return_count"] - 1))

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_return_count_plenty(self):
        return self._recursion_scene(0, other_count=self.card.effect_params["return_count"] + 2)

