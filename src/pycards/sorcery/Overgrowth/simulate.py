from game.card_simulation import bind_card, simulate, Card_Simulation
from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.sorcery.Overgrowth.model import Overgrowth


@bind_card(Overgrowth)
class Overgrowth_Simulation(Card_Simulation):
    scenario_locks={
        '_resource_scene':('opponent.land_area', 'self.graveyard', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "land.effect": [
            "Put the first land in your library onto your battlefield tapped, if there is one.",
            "If your library contains a land, move its earliest land onto your battlefield tapped.",
            "Find the first land in library order and put it onto your battlefield tapped.",
            "Move the earliest land from your library into play tapped, if available.",
            "If any land remains in your library, put the first one onto your battlefield tapped.",
            "Put your library's earliest land into play tapped when one is available.",
            "Scan your library in order and move the first land onto your battlefield tapped.",
            "The first land in your library enters your battlefield tapped, if present.",
            "From the library, move the first available land into play tapped.",
            "Put the earliest available land in your library onto your battlefield in a tapped state.",
        ],
        "land.untap": [
            "Then untap your first tapped land, if any.",
            "Afterward, untap the earliest tapped land you control.",
            "Untap the first tapped land in your land area, if present.",
            "Next, untap one tapped land, taking the first in land order.",
            "If you have a tapped land, untap the first one.",
            "Then untap your earliest land that is tapped.",
            "Untap the first available tapped land on your battlefield.",
            "Following the land step, untap your first tapped land.",
            "Go through your lands in order and untap the first tapped one.",
            "Afterward, your earliest tapped land becomes untapped.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _resource_scene(self,basics,other_cards=3,nonbasic=False,tapped=0,missing=1):
        self.scenario_prepare()
        self.player.life = max(1, self.player.ini_life - missing)
        self.player.graveyard.clear()
        self.scenario_replace_cards(self.player,"library",instant=(other_cards, other_cards))
        self.player.library = [card for card in self.player.library if card.type == "Instant"][:other_cards]
        for _ in range(basics):
            self.player.library.append(Plains(self.player))
        if nonbasic:
            land = self.scenario_cards(self.player,land=1,basic=False)[0]
            self.player.library.insert(0, land)
        for index in range(tapped):
            land = Plains(self.player)
            self.scenario_tapped(land)
            self.stage_card(land, zone="land_area")
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('land.effect', 'land.untap'), 'fields': ('mana_cost',)})
    def simulate_basic_none(self):
        return self._resource_scene(0)

    @simulate(evidence={'text': ('land.effect', 'land.untap'), 'fields': ('mana_cost',)})
    def simulate_basic_one(self):
        return self._resource_scene(1)

    @simulate(evidence={'text': ('land.effect', 'land.untap'), 'fields': ('mana_cost',)})
    def simulate_basic_several(self):
        return self._resource_scene(4)

    @simulate(evidence={'text': ('land.effect', 'land.untap'), 'fields': ('mana_cost',)})
    def simulate_nonbasic_first(self):
        return self._resource_scene(2,nonbasic=True)

    @simulate(evidence={'text': ('land.effect', 'land.untap'), 'fields': ('mana_cost',)})
    def simulate_empty_library(self):
        return self._resource_scene(0,other_cards=0)

    @simulate(evidence={'text': ('land.effect', 'land.untap'), 'fields': ('mana_cost',)})
    def simulate_only_basic_library(self):
        return self._resource_scene(1,other_cards=0)

    @simulate(evidence={'text': ('land.effect', 'land.untap'), 'fields': ('mana_cost',)})
    def simulate_tapped_0(self):
        return self._resource_scene(1,tapped=0)

    @simulate(evidence={'text': ('land.effect', 'land.untap'), 'fields': ('mana_cost',)})
    def simulate_tapped_1(self):
        return self._resource_scene(1,tapped=1)

    @simulate(evidence={'text': ('land.effect', 'land.untap'), 'fields': ('mana_cost',)})
    def simulate_tapped_3(self):
        return self._resource_scene(1,tapped=3)

