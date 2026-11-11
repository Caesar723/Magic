from game.card_simulation import bind_card, simulate, Card_Simulation
from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.sorcery.Harvest_Blessing.model import Harvest_Blessing


@bind_card(Harvest_Blessing)
class Harvest_Blessing_Simulation(Card_Simulation):
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
        "buff.stats": [
            "It gets +{power_bonus}/+{toughness_bonus} until that creature's controller's turn ends.",
            "Give it +{power_bonus}/+{toughness_bonus} until that creature's controller's turn ends.",
            "It gains +{power_bonus}/+{toughness_bonus} until that creature's controller's turn ends.",
            "Until that creature's controller's turn ends, it gets +{power_bonus}/+{toughness_bonus}.",
            "Increase its power by {power_bonus} and toughness by {toughness_bonus} until that creature's controller's turn ends.",
            "It receives +{power_bonus}/+{toughness_bonus} until that creature's controller's turn ends.",
            "Its power increases by {power_bonus} and its toughness by {toughness_bonus} until that creature's controller's turn ends.",
            "Grant it +{power_bonus}/+{toughness_bonus} until that creature's controller's turn ends.",
            "It gets an extra {power_bonus} power and {toughness_bonus} toughness until that creature's controller's turn ends.",
            "Until that creature's controller's turn ends, add {power_bonus} to its power and {toughness_bonus} to its toughness.",
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
        if forest:
            self.stage_card(Forest(self.player), zone="land_area")
        subaction = 0
        if role != "none":
            owner = self.player.opponent if role.startswith("enemy") else self.player
            flags = {"Hexproof": role.endswith("hexproof"), "Trample": role.endswith("trample")}
            self.scenario_creature(owner, power=2, health=3, flags=flags)
            subaction = 1 if owner is self.player.opponent else 11
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast((subaction,), provide_mana=False)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_basic_none(self):
        return self._resource_scene(0, role="self")

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_basic_one(self):
        return self._resource_scene(1, role="self")

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_basic_several(self):
        return self._resource_scene(4, role="self")

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_nonbasic_first(self):
        return self._resource_scene(2, nonbasic=True, role="self")

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_empty_library(self):
        return self._resource_scene(0, other_cards=0, role="self")

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_only_basic_library(self):
        return self._resource_scene(1, other_cards=0, role="self")

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_self_forest_False(self):
        return self._resource_scene(3, role='self', forest=False)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_enemy_forest_False(self):
        return self._resource_scene(3, role='enemy', forest=False)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_none_forest_False(self):
        return self._resource_scene(3, role='none', forest=False)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_self_trample_forest_False(self):
        return self._resource_scene(3, role='self_trample', forest=False)

    @simulate(evidence={'text': ('land.effect', 'buff.stats'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof_forest_False(self):
        return self._resource_scene(3, role='enemy_hexproof', forest=False)

