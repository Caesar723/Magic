from game.card_simulation import bind_card, simulate, Card_Simulation
from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.sorcery.Forest_s_Embrace.model import Forest_s_Embrace


@bind_card(Forest_s_Embrace)
class Forest_s_Embrace_Simulation(Card_Simulation):
    text_parts = {
        "land.effect": [
            "Put {land_count} random basic lands from your library onto your battlefield tapped, or all available if fewer.",
            "Randomly take up to {land_count} basic lands from your library and put them into play tapped, taking all if fewer exist.",
            "Choose {land_count} basic lands at random from your library, or all if fewer, and put them onto your battlefield tapped.",
            "Move {land_count} randomly selected basic lands from your library into play tapped, limited by availability.",
            "Randomly select as many as {land_count} basic lands in your library and put all selected lands onto your battlefield tapped.",
            "Put up to {land_count} basic lands chosen randomly from your library into play tapped, taking as many as available.",
            "Repeat {land_count} times, putting a random available basic land from your library onto your battlefield tapped.",
            "For {land_count} attempts, move one random basic land from your library into play tapped whenever available.",
            "Take {land_count} random basic lands from the library if available and put them onto your battlefield tapped, or take all if fewer.",
            "Move as many available basic lands as possible, up to {land_count}, randomly from your library into play tapped.",
        ],
        "library.shuffle": [
            "Then shuffle your library.",
            "Shuffle the remaining library afterward.",
            "Next, shuffle your remaining library.",
            "Afterward, shuffle the library.",
            "Finish by shuffling your library.",
            "Finally, randomize your library's order.",
            "Shuffle your library after this.",
            "After moving the land, shuffle your library.",
            "Then randomize the order of your remaining library.",
            "The remaining library is shuffled afterward.",
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

