from game.card_simulation import bind_card, simulate, Card_Simulation
from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.sorcery.Arcane_Convergence.model import Arcane_Convergence


@bind_card(Arcane_Convergence)
class Arcane_Convergence_Simulation(Card_Simulation):
    scenario_locks={
        '_resource_scene':('opponent.land_area', 'self.graveyard', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "land.untap": [
            "Untap all tapped lands you control.",
            "Then untap all tapped lands you control.",
            "You untap all tapped lands you control.",
            "Now untap all tapped lands you control.",
            "Immediately untap all tapped lands you control.",
            "First untap all tapped lands you control.",
            "Begin by untapping all tapped lands you control.",
            "Start by untapping all tapped lands you control.",
            "Fully untap all tapped lands you control.",
            "Proceed to untap all tapped lands you control.",
        ],
        "mana.effect": [
            "For each sorcery card in your graveyard, add one mana, cycling through U, B, R, G, W in that order.",
            "Count your graveyard sorceries and add that many mana in repeating U, B, R, G, W order.",
            "Add one mana per sorcery in your graveyard, assigning colors cyclically as U, B, R, G, W.",
            "Generate mana equal to your graveyard sorcery count, using U then B then R then G then W repeatedly.",
            "Each graveyard sorcery grants one mana, with colors cycling U, B, R, G, W.",
            "For your graveyard sorceries, produce one mana each in U, B, R, G, W cycles.",
            "Add as many mana as you have sorceries in your graveyard, distributing them in U, B, R, G, W order repeatedly.",
            "Your graveyard sorcery count determines mana gained in a repeating U, B, R, G, W sequence.",
            "Gain one mana for each sorcery in your graveyard, following the repeating sequence U, B, R, G, W.",
            "Produce one mana per graveyard sorcery and cycle the colors through U, B, R, G, W.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _resource_scene(self,basics,other_cards=3,nonbasic=False,tapped=0,missing=1,grave_count=0):
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
        self.scenario_cards(self.player,zone="graveyard",instant=grave_count,safe=True)
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_basic_none(self):
        return self._resource_scene(0)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_basic_one(self):
        return self._resource_scene(1)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_basic_several(self):
        return self._resource_scene(4)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_nonbasic_first(self):
        return self._resource_scene(2,nonbasic=True)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_library(self):
        return self._resource_scene(0,other_cards=0)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_only_basic_library(self):
        return self._resource_scene(1,other_cards=0)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_0_tapped_0(self):
        return self._resource_scene(0,grave_count=0,tapped=0)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_0_tapped_3(self):
        return self._resource_scene(0,grave_count=0,tapped=3)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_1_tapped_0(self):
        return self._resource_scene(0,grave_count=1,tapped=0)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_1_tapped_3(self):
        return self._resource_scene(0,grave_count=1,tapped=3)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_4_tapped_0(self):
        return self._resource_scene(0,grave_count=4,tapped=0)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_4_tapped_3(self):
        return self._resource_scene(0,grave_count=4,tapped=3)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_5_tapped_0(self):
        return self._resource_scene(0,grave_count=5,tapped=0)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_5_tapped_3(self):
        return self._resource_scene(0,grave_count=5,tapped=3)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_6_tapped_0(self):
        return self._resource_scene(0,grave_count=6,tapped=0)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_6_tapped_3(self):
        return self._resource_scene(0,grave_count=6,tapped=3)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_9_tapped_0(self):
        return self._resource_scene(0,grave_count=9,tapped=0)

    @simulate(evidence={'text': ('land.untap', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_sorceries_9_tapped_3(self):
        return self._resource_scene(0,grave_count=9,tapped=3)

