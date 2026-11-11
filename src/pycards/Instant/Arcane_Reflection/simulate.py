from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Arcane_Reflection.model import Arcane_Reflection


@bind_card(Arcane_Reflection)
class Arcane_Reflection_Simulation(Card_Simulation):
    scenario_locks={
        '_recursion_scene':('opponent.graveyard', 'opponent.hand', 'self.graveyard', 'self.hand', 'self.library'),
    }

    text_parts = {
        "return.effect": [
            "Put a random instant or sorcery card other than this card from your graveyard into your hand, if available.",
            "If there is a instant or sorcery card other than this card from your graveyard, choose one randomly and put it into your hand.",
            "Choose a instant or sorcery card other than this card from your graveyard at random and move it into your hand, if possible.",
            "Move one random instant or sorcery card other than this card from your graveyard into your hand when available.",
            "Randomly select a instant or sorcery card other than this card from your graveyard and put that card into your hand, if one exists.",
            "When any instant or sorcery card other than this card from your graveyard is available, choose one at random to move into your hand.",
            "Put one available instant or sorcery card other than this card from your graveyard, chosen randomly, into your hand.",
            "If possible, take a instant or sorcery card other than this card from your graveyard chosen at random and put it into your hand.",
            "Move a randomly chosen instant or sorcery card other than this card from your graveyard into your hand if any are available.",
            "Take a random instant or sorcery card other than this card from your graveyard and move it into your hand, when one exists.",
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

