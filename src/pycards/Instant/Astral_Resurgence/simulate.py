from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Astral_Resurgence.model import Astral_Resurgence


@bind_card(Astral_Resurgence)
class Astral_Resurgence_Simulation(Card_Simulation):
    scenario_locks={
        '_recursion_scene':('opponent.graveyard', 'opponent.hand', 'self.graveyard', 'self.hand', 'self.library'),
    }

    text_parts = {
        "return.effect": [
            "Put a fresh copy of a random creature in your graveyard onto your battlefield, leaving the original in your graveyard.",
            "Choose a creature in your graveyard randomly and create a fresh battlefield copy, retaining the original graveyard card.",
            "Copy a random creature card from your graveyard onto your battlefield without moving the original.",
            "Create a fresh copy on your battlefield of a random graveyard creature you own, leaving that card in the graveyard.",
            "Randomly select a creature in your graveyard and put its fresh copy into play while keeping the original in the graveyard.",
            "Put a fresh battlefield copy of a randomly chosen creature from your graveyard into play and keep the original card there.",
            "If a creature is available in your graveyard, put a random one's fresh copy onto your battlefield and retain the original.",
            "Create a fresh battlefield copy from one random creature in your graveyard without removing that graveyard card.",
            "Choose a random creature card from your graveyard to copy onto your battlefield, preserving the original in the graveyard.",
            "Put a fresh copy of one randomly selected graveyard creature onto your battlefield while the original stays in your graveyard.",
        ],
        "return.lifelink": [
            "The new copy gains lifelink until your end step.",
            "Give that copy lifelink until your turn ends.",
            "Until your end step, the returned copy has lifelink.",
            "Grant the new creature lifelink through your turn.",
            "The copy receives lifelink until the end of your turn.",
            "That new battlefield copy gains lifelink until your end step.",
            "Until your turn ends, the newly created creature has lifelink.",
            "Give lifelink to the new copy until your end step.",
            "The newly created creature is granted lifelink until your turn ends.",
            "The copy gets the lifelink ability until your end step.",
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

    @simulate(evidence={'text': ('return.effect', 'return.lifelink'), 'fields': ('mana_cost',)})
    def simulate_graves_none(self):
        return self._recursion_scene(0, 0, 0)

    @simulate(evidence={'text': ('return.effect', 'return.lifelink'), 'fields': ('mana_cost',)})
    def simulate_graves_one_own(self):
        return self._recursion_scene(1, 0, 0)

    @simulate(evidence={'text': ('return.effect', 'return.lifelink'), 'fields': ('mana_cost',)})
    def simulate_graves_one_enemy(self):
        return self._recursion_scene(0, 1, 0)

    @simulate(evidence={'text': ('return.effect', 'return.lifelink'), 'fields': ('mana_cost',)})
    def simulate_graves_both(self):
        return self._recursion_scene(1, 1, 0)

    @simulate(evidence={'text': ('return.effect', 'return.lifelink'), 'fields': ('mana_cost',)})
    def simulate_graves_several(self):
        return self._recursion_scene(3, 3, 0)

    @simulate(evidence={'text': ('return.effect', 'return.lifelink'), 'fields': ('mana_cost',)})
    def simulate_graves_noncreatures(self):
        return self._recursion_scene(0, 0, 3)

    @simulate(evidence={'text': ('return.effect', 'return.lifelink'), 'fields': ('mana_cost',)})
    def simulate_graves_mixed(self):
        return self._recursion_scene(3, 3, 3)

