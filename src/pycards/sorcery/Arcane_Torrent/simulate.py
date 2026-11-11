from game.card_simulation import bind_card, simulate, Card_Simulation
from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.sorcery.Arcane_Torrent.model import Arcane_Torrent


@bind_card(Arcane_Torrent)
class Arcane_Torrent_Simulation(Card_Simulation):
    text_parts = {
        "search.effect": [
            "Put a random sorcery card from your library into your hand, if one is available.",
            "If your library has a sorcery card, randomly choose one and put it into your hand.",
            "Choose a sorcery card from your library at random and put it into your hand, if possible.",
            "If available, move one random sorcery card from your library into your hand.",
            "Randomly select a sorcery card in your library and put it into your hand, when available.",
            "When your library contains a sorcery card, put one selected at random into your hand.",
            "Move a randomly chosen sorcery card from your library into your hand if any exist.",
            "Put one sorcery card chosen randomly from your library into your hand, if you have one.",
            "From your library, take a random sorcery card if present and put it into your hand.",
            "If any sorcery cards remain in your library, randomly choose one to enter your hand.",
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
        for _ in range(basics):
            self.player.library.append(self.card.copy_for_player(self.player))
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('search.effect',), 'fields': ('mana_cost',)})
    def simulate_basic_none(self):
        return self._resource_scene(0)

    @simulate(evidence={'text': ('search.effect',), 'fields': ('mana_cost',)})
    def simulate_basic_one(self):
        return self._resource_scene(1)

    @simulate(evidence={'text': ('search.effect',), 'fields': ('mana_cost',)})
    def simulate_basic_several(self):
        return self._resource_scene(4)

    @simulate(evidence={'text': ('search.effect',), 'fields': ('mana_cost',)})
    def simulate_nonbasic_first(self):
        return self._resource_scene(2, nonbasic=True)

    @simulate(evidence={'text': ('search.effect',), 'fields': ('mana_cost',)})
    def simulate_empty_library(self):
        return self._resource_scene(0, other_cards=0)

    @simulate(evidence={'text': ('search.effect',), 'fields': ('mana_cost',)})
    def simulate_only_basic_library(self):
        return self._resource_scene(1, other_cards=0)

