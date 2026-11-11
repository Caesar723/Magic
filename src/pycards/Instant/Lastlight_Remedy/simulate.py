import random

from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Lastlight_Remedy.model import Lastlight_Remedy


@bind_card(Lastlight_Remedy)
class Lastlight_Remedy_Simulation(Card_Simulation):
    scenario_locks={
        '_simulate_life':('self.hand', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "low.condition": [
            "If you have {life_threshold} or less life,",
            "If your life total is {life_threshold} or less,",
            "If your life total is at most {life_threshold},",
            "If you have no more than {life_threshold} life,",
            "If your life total is no greater than {life_threshold},",
            "If your life total does not exceed {life_threshold},",
            "If you have {life_threshold} life or fewer,",
            "If your life total is equal to or below {life_threshold},",
            "If you have a life total of {life_threshold} or less,",
            "If your life total is less than or equal to {life_threshold},",
        ],
        "low.heal": [
            "you gain {heal_low} life",
            "gain {heal_low} life",
            "you gain a total of {heal_low} life",
            "gain a total of {heal_low} life",
            "increase your life total by {heal_low}",
            "you increase your life total by {heal_low}",
            "restore {heal_low} life",
            "you restore {heal_low} life",
            "gain an amount of life equal to {heal_low}",
            "you gain an amount of life equal to {heal_low}",
        ],
        "low.draw": [
            "and draw {draw_count} cards.",
            "and then draw {draw_count} cards.",
            "and draw a total of {draw_count} cards.",
            "and then draw a total of {draw_count} cards.",
            "and draw {draw_count} cards from your library.",
            "and then draw {draw_count} cards from your library.",
            "and also draw {draw_count} cards.",
            "and also draw a total of {draw_count} cards.",
            "and draw a total of {draw_count} cards from your library.",
            "and then draw a total of {draw_count} cards from your library.",
        ],
        "high.condition": [
            "Otherwise,",
            "Otherwise, instead,",
            "If the first condition was false,",
            "If the initial condition was not met,",
            "If the life-total condition was false,",
            "If you had more than {life_threshold} life when this effect began,",
            "If your life total was above {life_threshold} when this effect began,",
            "If you had over {life_threshold} life before these effects,",
            "If your life total initially exceeded {life_threshold},",
            "If your life total was greater than {life_threshold} before these effects,",
        ],
        "high.heal": [
            "you gain {heal_normal} life.",
            "gain {heal_normal} life.",
            "you gain a total of {heal_normal} life.",
            "gain a total of {heal_normal} life.",
            "increase your life total by {heal_normal}.",
            "you increase your life total by {heal_normal}.",
            "restore {heal_normal} life.",
            "you restore {heal_normal} life.",
            "gain an amount of life equal to {heal_normal}.",
            "you gain an amount of life equal to {heal_normal}.",
        ],
    }

    def _simulate_life(self, life, library_count=None, empty_hand=False, low_branch=None):
        library_count=self.scenario_count("library",library_count)
        params = self.card.effect_params
        self.text_parts = dict(type(self).text_parts)
        if params["draw_count"] == 1:
            self.text_parts["low.draw"] = [
                phrase.replace("cards", "card") for phrase in self.text_parts["low.draw"]
            ]

        valid_life = 1 <= life <= self.player.ini_life
        valid_branch = low_branch is None or (life <= params["life_threshold"]) == low_branch
        if not (valid_life and valid_branch):
            return {"card": self.card, "type": 0, "action": None}

        library_count = params["draw_count"] + 2 if library_count is None else library_count
        self.scenario_prepare({
            "graveyard": {"creature_number": (0, 0), "instant_number": (0, 0), "sorcery_number": (0, 0), "land_number": (0, 0)},
            "hand": {"creature_number": (0, 1), "instant_number": (0, 1), "sorcery_number": (0, 1), "land_number": (0, 1)},
            "library": {"creature_number": (0, 0), "instant_number": (0, 0), "sorcery_number": (0, 0), "land_number": (library_count, library_count)},
        })
        self.player.library = self.player.library[:library_count]
        if empty_hand:
            self.player.hand = []

        self.random_life()(self.player.opponent)
        self.player.life = life
        self.room.env_mana(
            self.player, {"W": (2, 5)}, least_mana=self.card.calculate_cost()
        )
        return self.room.simulate_play(self.card, preferred_subactions=(0,))

    @simulate(evidence={'text': ('low.condition', 'low.heal', 'low.draw'), 'fields': ('mana_cost',)})
    def simulate_below_threshold(self):
        return self._simulate_life(self.card.effect_params["life_threshold"] - 1, low_branch=True)

    @simulate(evidence={'text': ('low.condition', 'low.heal', 'low.draw'), 'fields': ('mana_cost',)})
    def simulate_at_threshold(self):
        return self._simulate_life(self.card.effect_params["life_threshold"], low_branch=True)

    @simulate(evidence={'text': ('low.condition', 'high.condition', 'high.heal'), 'fields': ('mana_cost',)})
    def simulate_above_threshold(self):
        return self._simulate_life(self.card.effect_params["life_threshold"] + 1, low_branch=False)

    @simulate(evidence={'text': ('low.condition', 'low.heal', 'low.draw'), 'fields': ('mana_cost',)})
    def simulate_minimum_life(self):
        return self._simulate_life(1, low_branch=True)

    @simulate(evidence={'text': ('low.condition', 'high.condition', 'high.heal'), 'fields': ('mana_cost',)})
    def simulate_near_full_life(self):
        return self._simulate_life(self.player.ini_life - 1, low_branch=False)

    @simulate(evidence={'text': ('low.condition', 'high.condition', 'high.heal'), 'fields': ('mana_cost',)})
    def simulate_full_life(self):
        return self._simulate_life(self.player.ini_life, low_branch=False)

    @simulate(evidence={'text': ('low.condition', 'low.heal', 'low.draw'), 'fields': ('mana_cost',)})
    def simulate_below_threshold_empty_library(self):
        return self._simulate_life(self.card.effect_params["life_threshold"] - 1, library_count=0, low_branch=True)

    @simulate(evidence={'text': ('low.condition', 'low.heal', 'low.draw'), 'fields': ('mana_cost',)})
    def simulate_at_threshold_empty_library(self):
        return self._simulate_life(self.card.effect_params["life_threshold"], library_count=0, low_branch=True)

    @simulate(evidence={'text': ('low.condition', 'low.heal', 'low.draw'), 'fields': ('mana_cost',)})
    def simulate_low_branch_short_library(self):
        return self._simulate_life(self.card.effect_params["life_threshold"], library_count=max(0, self.card.effect_params["draw_count"] - 1), low_branch=True)

    @simulate(evidence={'text': ('low.condition', 'low.heal', 'low.draw'), 'fields': ('mana_cost',)})
    def simulate_low_branch_exact_library(self):
        return self._simulate_life(self.card.effect_params["life_threshold"], library_count=self.card.effect_params["draw_count"], low_branch=True)

    @simulate(evidence={'text': ('low.condition', 'high.condition', 'high.heal'), 'fields': ('mana_cost',)})
    def simulate_above_threshold_empty_library(self):
        return self._simulate_life(self.card.effect_params["life_threshold"] + 1, library_count=0, low_branch=False)

    @simulate(evidence={'text': ('low.condition', 'low.heal', 'low.draw'), 'fields': ('mana_cost',)})
    def simulate_low_branch_no_other_hand_cards(self):
        return self._simulate_life(self.card.effect_params["life_threshold"], empty_hand=True, low_branch=True)

    @simulate(evidence={'text': ('low.condition', 'high.condition', 'high.heal'), 'fields': ('mana_cost',)})
    def simulate_high_branch_no_other_hand_cards(self):
        return self._simulate_life(self.card.effect_params["life_threshold"] + 1, empty_hand=True, low_branch=False)

    @simulate(evidence={'text': ('low.condition', 'low.heal', 'low.draw', 'high.condition', 'high.heal'), 'fields': ('mana_cost',)})
    def simulate_random_life_and_library(self):
        return self._simulate_life(random.randint(1, self.player.ini_life), library_count=random.randint(0, self.card.effect_params["draw_count"] + 2))

