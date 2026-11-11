from game.card_simulation import bind_card, simulate, Card_Simulation
from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.sorcery.Verdant_Harvest.model import Verdant_Harvest


@bind_card(Verdant_Harvest)
class Verdant_Harvest_Simulation(Card_Simulation):
    text_parts = {
        "land.effect": [
            "Put a basic land you choose from your library onto your battlefield tapped, if one is available.",
            "If your library has a basic land, choose one and put it onto your battlefield tapped.",
            "Choose a basic land from your library of your choice and put it into play tapped, if possible.",
            "If available, move one chosen basic land from your library onto your battlefield tapped.",
            "Choose a basic land in your library and put it onto your battlefield tapped, when available.",
            "When your library contains a basic land, put one selected of your choice into play tapped.",
            "Move a chosen basic land from your library onto your battlefield tapped if any exist.",
            "Put one basic land you choose from your library into play tapped, if you have one.",
            "From your library, take a basic land you choose if present and put it onto your battlefield tapped.",
            "If any basic lands remain in your library, choose one to enter your battlefield tapped.",
        ],
        "draw.effect": [
            "If a basic land was put into play this way, draw {draw_count} card{draw_count_plural}.",
            "If a basic land was put into play this way, draw {draw_count_word} card{draw_count_plural}.",
            "If a basic land was put into play this way, take the top {draw_count} card{draw_count_plural} of your library into your hand.",
            "If a basic land was put into play this way, put the top {draw_count} card{draw_count_plural} from your library into your hand.",
            "If a basic land was put into play this way, add the top {draw_count} card{draw_count_plural} of your library to your hand.",
            "If a basic land was put into play this way, you draw {draw_count} card{draw_count_plural}.",
            "If a basic land was put into play this way, draw a total of {draw_count} card{draw_count_plural}.",
            "If a basic land was put into play this way, you draw a total of {draw_count_word} card{draw_count_plural}.",
            "If a basic land was put into play this way, take {draw_count} card{draw_count_plural} from the top of your library into your hand.",
            "If a basic land was put into play this way, put {draw_count} card{draw_count_plural} from the top of your library into your hand.",
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

    @simulate(evidence={'text': ('land.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_basic_none(self):
        return self._resource_scene(0)

    @simulate(evidence={'text': ('land.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_basic_one(self):
        return self._resource_scene(1)

    @simulate(evidence={'text': ('land.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_basic_several(self):
        return self._resource_scene(4)

    @simulate(evidence={'text': ('land.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_nonbasic_first(self):
        return self._resource_scene(2, nonbasic=True)

    @simulate(evidence={'text': ('land.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_library(self):
        return self._resource_scene(0, other_cards=0)

    @simulate(evidence={'text': ('land.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_only_basic_library(self):
        return self._resource_scene(1, other_cards=0)

    @simulate(evidence={'text': ('land.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_tail(self):
        return self._resource_scene(1, other_cards=0)

    @simulate(evidence={'text': ('land.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_short_tail(self):
        return self._resource_scene(1, other_cards=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('land.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_exact_tail(self):
        return self._resource_scene(1, other_cards=self.card.effect_params["draw_count"])

