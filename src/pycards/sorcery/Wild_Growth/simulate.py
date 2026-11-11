from game.card_simulation import bind_card, simulate, Card_Simulation
from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.sorcery.Wild_Growth.model import Wild_Growth


@bind_card(Wild_Growth)
class Wild_Growth_Simulation(Card_Simulation):
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
        "library.scry": [
            "Then scry {scry_count}.",
            "Afterward, scry {scry_count}.",
            "Next, scry {scry_count}.",
            "You then scry {scry_count}.",
            "Finish by scrying {scry_count}.",
            "Finally, scry {scry_count}.",
            "After the land step, scry {scry_count}.",
            "Follow this by scrying {scry_count}.",
            "Afterward, you scry {scry_count}.",
            "The land step is followed by scry {scry_count}.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _resource_scene(self, basics, other_cards=3, nonbasic=False, role="none", forest=False, tapped=0, missing=1, grave_count=0):
        self.scenario_prepare()
        self.player.life = max(1, self.player.ini_life - missing)
        self.player.graveyard.clear()
        self.room.env_initinal_library(self.player, {"instant_number": (other_cards, other_cards), "creature_number": (0, 0), "sorcery_number": (0, 0), "land_number": (0, 0)})
        self.player.library = [card for card in self.player.library if card.type == "Instant"][:other_cards]
        for _ in range(basics):
            self.player.library.append(Plains(self.player))
        if nonbasic:
            land = Land(self.player)
            land.name, land.type = "Review nonbasic land", "Land"
            self.player.library.insert(0, land)
        for index in range(tapped):
            land = Plains(self.player)
            land.tap()
            self.stage_card(land, zone="land_area")
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('land.effect', 'library.scry'), 'fields': ('mana_cost',)})
    def simulate_basic_none(self):
        return self._resource_scene(0)

    @simulate(evidence={'text': ('land.effect', 'library.scry'), 'fields': ('mana_cost',)})
    def simulate_basic_one(self):
        return self._resource_scene(1)

    @simulate(evidence={'text': ('land.effect', 'library.scry'), 'fields': ('mana_cost',)})
    def simulate_basic_several(self):
        return self._resource_scene(4)

    @simulate(evidence={'text': ('land.effect', 'library.scry'), 'fields': ('mana_cost',)})
    def simulate_nonbasic_first(self):
        return self._resource_scene(2, nonbasic=True)

    @simulate(evidence={'text': ('land.effect', 'library.scry'), 'fields': ('mana_cost',)})
    def simulate_empty_library(self):
        return self._resource_scene(0, other_cards=0)

    @simulate(evidence={'text': ('land.effect', 'library.scry'), 'fields': ('mana_cost',)})
    def simulate_only_basic_library(self):
        return self._resource_scene(1, other_cards=0)

    @simulate(evidence={'text': ('land.effect', 'library.scry'), 'fields': ('mana_cost',)})
    def simulate_empty_tail(self):
        return self._resource_scene(1, other_cards=0)

    @simulate(evidence={'text': ('land.effect', 'library.scry'), 'fields': ('mana_cost',)})
    def simulate_short_tail(self):
        return self._resource_scene(1, other_cards=max(0, self.card.effect_params["scry_count"] - 1))

    @simulate(evidence={'text': ('land.effect', 'library.scry'), 'fields': ('mana_cost',)})
    def simulate_exact_tail(self):
        return self._resource_scene(1, other_cards=self.card.effect_params["scry_count"])

