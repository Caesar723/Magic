from game.card_simulation import bind_card, simulate, Card_Simulation
from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.sorcery.Verdant_Genesis.model import Verdant_Genesis


@bind_card(Verdant_Genesis)
class Verdant_Genesis_Simulation(Card_Simulation):
    text_parts = {
        "land.effect": [
            "Put the first {land_count} lands in your library onto your battlefield tapped, or all if fewer remain.",
            "Move up to {land_count} lands from your library into play tapped, taking them in library order.",
            "Find the earliest {land_count} lands in your library and put all available ones onto your battlefield tapped.",
            "Put your library's first {land_count} available lands into play tapped.",
            "Take lands in library order, up to {land_count}, and put them onto your battlefield tapped.",
            "Move the earliest available lands from your library into play tapped, stopping after {land_count}.",
            "Scan your library in order and put the first {land_count} available lands onto your battlefield tapped.",
            "The first available {land_count} lands in your library enter your battlefield tapped.",
            "Move lands from your library onto your battlefield tapped in their existing order, up to {land_count}.",
            "Put up to {land_count} of the earliest lands in your library into play tapped, taking all if fewer remain.",
        ],
        "buff.stats": [
            "Give each creature you control +{power_bonus}/+{toughness_bonus} permanently.",
            "Also give each creature you control +{power_bonus}/+{toughness_bonus} permanently.",
            "Then give each creature you control +{power_bonus}/+{toughness_bonus} permanently.",
            "You give each creature you control +{power_bonus}/+{toughness_bonus} permanently.",
            "Now give each creature you control +{power_bonus}/+{toughness_bonus} permanently.",
            "Immediately give each creature you control +{power_bonus}/+{toughness_bonus} permanently.",
            "Additionally give each creature you control +{power_bonus}/+{toughness_bonus} permanently.",
            "Finally give each creature you control +{power_bonus}/+{toughness_bonus} permanently.",
            "With this effect give each creature you control +{power_bonus}/+{toughness_bonus} permanently.",
            "After the land step give each creature you control +{power_bonus}/+{toughness_bonus} permanently.",
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
        for owner in (self.player, self.player.opponent):
            for index in range(3):
                self.scenario_creature(owner, power=index + 1, health=index + 2, flags={})
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_basic_none(self):
        return self._resource_scene(0)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_basic_one(self):
        return self._resource_scene(1)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_basic_several(self):
        return self._resource_scene(4)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_nonbasic_first(self):
        return self._resource_scene(2, nonbasic=True)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_empty_library(self):
        return self._resource_scene(0, other_cards=0)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_only_basic_library(self):
        return self._resource_scene(1, other_cards=0)

