from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Primal_Surge.model import Primal_Surge


@bind_card(Primal_Surge)
class Primal_Surge_Simulation(Card_Simulation):
    scenario_locks={
        '_resource_scene':('self.hand', 'self.library'),
    }

    text_parts = {
        "hand.effect": [
            "For each card currently in your hand, move that card to the bottom of your library and immediately draw one card.",
            "Process your current hand cards one at a time, placing each at the library bottom and drawing one after each move.",
            "For every current hand card in order, put it on your library's bottom and then draw a card immediately.",
            "Move the cards presently in your hand to the library bottom one by one, drawing one card after every move.",
            "Take each card from your initial hand in order, place it at the library bottom, and draw once before continuing.",
            "One at a time, send each of your current hand cards to the library bottom and draw a card after sending it.",
            "Put every currently held card on the library bottom in sequence, drawing one immediately after each card.",
            "Cycle each initial hand card through the library bottom, drawing one card after every insertion.",
            "For each card in your hand when this resolves, place it beneath the library and immediately draw one.",
            "Go through your current hand in order, bottom each card in your library, and draw one after each bottoming.",
        ],
        "land.effect": [
            "Increase your land-play limit by {extra_lands} until your end step.",
            "You may play {extra_lands} additional lands until your turn ends.",
            "Add {extra_lands} to your land-play limit until your end step.",
            "Your land-play limit increases by {extra_lands} until the end of your turn.",
            "Until your end step, you receive {extra_lands} extra land plays.",
            "Give yourself {extra_lands} additional permitted land plays through your turn.",
            "Raise your land-play allowance by {extra_lands} until your end step.",
            "Until your turn ends, add {extra_lands} to your maximum land plays.",
            "Grant {extra_lands} extra land plays until your end step.",
            "Your maximum land plays rises by {extra_lands} until your turn ends.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _resource_scene(self,library_count=None,hand_count=None):
        self.scenario_prepare()
        self.scenario_random_cards(self.player,"library",library_count)
        self.scenario_random_cards(self.player,"hand",hand_count)
        return self.scenario_cast()

    @simulate(evidence={'text': ('hand.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_random_resources(self):
        return self._resource_scene()



    @simulate(evidence={'text': ('hand.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_0_hand_0(self):
        return self._resource_scene(library_count=0,hand_count=0)

    @simulate(evidence={'text': ('hand.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_0_hand_1(self):
        return self._resource_scene(library_count=0,hand_count=1)

    @simulate(evidence={'text': ('hand.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_0_hand_3(self):
        return self._resource_scene(library_count=0,hand_count=3)

    @simulate(evidence={'text': ('hand.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_1_hand_0(self):
        return self._resource_scene(library_count=1,hand_count=0)

    @simulate(evidence={'text': ('hand.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_1_hand_1(self):
        return self._resource_scene(library_count=1,hand_count=1)

    @simulate(evidence={'text': ('hand.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_1_hand_3(self):
        return self._resource_scene(library_count=1,hand_count=3)

    @simulate(evidence={'text': ('hand.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_3_hand_0(self):
        return self._resource_scene(library_count=3,hand_count=0)

    @simulate(evidence={'text': ('hand.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_3_hand_1(self):
        return self._resource_scene(library_count=3,hand_count=1)

    @simulate(evidence={'text': ('hand.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_3_hand_3(self):
        return self._resource_scene(library_count=3,hand_count=3)

