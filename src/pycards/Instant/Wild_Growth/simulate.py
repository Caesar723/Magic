from game.card_simulation import bind_card, simulate, Card_Simulation
from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.Instant.Wild_Growth.model import Wild_Growth


@bind_card(Wild_Growth)
class Wild_Growth_Simulation(Card_Simulation):
    text_parts = {
        "land.effect": [
            "Put a random basic land from your library onto your battlefield tapped, if one is available.",
            "If your library has a basic land, randomly choose one and put it onto your battlefield tapped.",
            "Choose a basic land from your library at random and put it into play tapped, if possible.",
            "If available, move one random basic land from your library onto your battlefield tapped.",
            "Randomly select a basic land in your library and put it onto your battlefield tapped, when available.",
            "When your library contains a basic land, put one selected at random into play tapped.",
            "Move a randomly chosen basic land from your library onto your battlefield tapped if any exist.",
            "Put one basic land chosen randomly from your library into play tapped, if you have one.",
            "From your library, take a random basic land if present and put it onto your battlefield tapped.",
            "If any basic lands remain in your library, randomly choose one to enter your battlefield tapped.",
        ],
        "library.shuffle": [
            "If a land was put into play this way, then shuffle your library.",
            "If a land was put into play this way, shuffle the remaining library afterward.",
            "If a land was put into play this way, next, shuffle your remaining library.",
            "If a land was put into play this way, afterward, shuffle the library.",
            "If a land was put into play this way, finish by shuffling your library.",
            "If a land was put into play this way, finally, randomize your library's order.",
            "If a land was put into play this way, shuffle your library after this.",
            "If a land was put into play this way, after moving the land, shuffle your library.",
            "If a land was put into play this way, then randomize the order of your remaining library.",
            "If a land was put into play this way, the remaining library is shuffled afterward.",
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

    @simulate(evidence={'text': ('land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_basic_none(self):
        return self._resource_scene(0)

    @simulate(evidence={'text': ('land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_basic_one(self):
        return self._resource_scene(1)

    @simulate(evidence={'text': ('land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_basic_several(self):
        return self._resource_scene(4)

    @simulate(evidence={'text': ('land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_nonbasic_first(self):
        return self._resource_scene(2, nonbasic=True)

    @simulate(evidence={'text': ('land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_empty_library(self):
        return self._resource_scene(0, other_cards=0)

    @simulate(evidence={'text': ('land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_only_basic_library(self):
        return self._resource_scene(1, other_cards=0)

