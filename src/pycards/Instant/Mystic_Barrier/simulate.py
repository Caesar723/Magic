from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Mystic_Barrier.model import Mystic_Barrier


@bind_card(Mystic_Barrier)
class Mystic_Barrier_Simulation(Card_Simulation):
    scenario_locks={
        '_resource_scene':('opponent.hand', 'opponent.library', 'self.hand', 'self.library'),
    }

    text_parts = {
        "lock.effect": [
            "Until your opponent's end step, prevent casting of noncreature cards currently in their hand.",
            "Noncreature cards now in your opponent's hand cannot be cast until that opponent's turn ends.",
            "Block casting of the opposing hand's current noncreature cards until your opponent's end step.",
            "Apply a casting lock to each noncreature card presently in the opposing hand until that player's turn ends.",
            "The noncreature cards your opponent holds now are uncastable until their end step.",
            "Until the opposing end step, prevent your opponent from casting their current noncreature hand cards.",
            "Each noncreature card currently in your opponent's hand receives a casting lock until that opponent's end step.",
            "Lock the current noncreature cards in the opposing hand against casting until that player's turn ends.",
            "Make the opponent's existing noncreature hand cards uncastable until their end step.",
            "Until your opponent ends their turn, their presently held noncreature cards cannot be cast.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _resource_scene(self,count,library_count=None,hand_count=None):
        library_count=self.scenario_count("library",library_count)
        hand_count=self.scenario_count("hand",hand_count,reserve=count)
        self.scenario_prepare()
        self.player.hand.clear()
        self.player.opponent.hand.clear()
        self.player.library.clear()
        for owner in (self.player, self.player.opponent):
            self.scenario_replace_cards(owner,"library",instant=(library_count, library_count))
            owner.library = [card for card in owner.library if card.type == "Instant"][:library_count]
        self.scenario_clear(self.player.opponent,"hand")
        self.scenario_random_cards(self.player.opponent,"hand",hand_count)
        subaction = 0
        for _ in range(count):
            creature = self.scenario_creature(self.player.opponent, power=2, health=3, flags={}, zone="hand")
        return self.scenario_cast()

    @simulate(evidence={'text': ('lock.effect',), 'fields': ('mana_cost',)})
    def simulate_count_0_normal(self):
        return self._resource_scene(0)

    @simulate(evidence={'text': ('lock.effect',), 'fields': ('mana_cost',)})
    def simulate_count_1_normal(self):
        return self._resource_scene(1)

    @simulate(evidence={'text': ('lock.effect',), 'fields': ('mana_cost',)})
    def simulate_count_3_normal(self):
        return self._resource_scene(3)

