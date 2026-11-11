from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.sorcery.Divine_Offering.model import Divine_Offering


@bind_card(Divine_Offering)
class Divine_Offering_Simulation(Card_Simulation):
    scenario_locks={
        '_land_scene':('opponent.hand', 'opponent.land_area'),
    }

    text_parts = {
        "target.scope": [
            "Choose a target opposing land.",
            "Target one opposing land.",
            "Select a opposing land as the target.",
            "Choose one opposing land to target.",
            "Select a target opposing land.",
            "Choose any opposing land as your target.",
            "Target a opposing land of your choice.",
            "Choose a opposing land as the target for this spell.",
            "Select one opposing land to target.",
            "Choose a opposing land as your target.",
        ],
        "remove.effect": [
            "Mark the selected opposing land for destruction.",
            "Set a destruction mark on the target opposing land.",
            "Apply a destruction mark to that opposing land.",
            "The selected opposing land is marked for destruction.",
            "Mark that land controlled by your opponent as destroyed.",
            "Flag the target opposing land as destroyed.",
            "Put a destruction flag on the selected opposing land.",
            "That opposing land receives a destruction mark.",
            "Place a destruction mark on the target land your opponent controls.",
            "The chosen opposing land is flagged for destruction.",
        ],
        "heal.effect": [
            "Your opponent gains {heal} life.",
            "The opposing player gains {heal} life.",
            "Your opponent gains a total of {heal} life.",
            "The opposing player gains a total of {heal} life.",
            "Increase your opponent's life total by {heal}.",
            "The opponent's life total increases by {heal}.",
            "Your opponent restores {heal} life.",
            "The opposing player restores {heal} life.",
            "Your opponent gains an amount of life equal to {heal}.",
            "The opposing player gains an amount of life equal to {heal}.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _land_scene(self, count, missing=1, hand_count=None):
        hand_count=self.scenario_count("hand",hand_count)
        self.scenario_prepare()
        self.room.env_mana(self.player.opponent, {"W": (count, count)})
        self.player.opponent.life = max(1, self.player.opponent.ini_life - missing)
        self.scenario_clear(self.player.opponent,"hand")
        self.scenario_random_cards(self.player.opponent,"hand",hand_count)
        return self.scenario_cast((1,))

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_0_lands_full(self):
        return self._land_scene(0, 0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_0_lands_near_full(self):
        return self._land_scene(0, 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_0_lands_injured(self):
        return self._land_scene(0, self.player.opponent.ini_life - 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_1_lands_full(self):
        return self._land_scene(1, 0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_1_lands_near_full(self):
        return self._land_scene(1, 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_1_lands_injured(self):
        return self._land_scene(1, self.player.opponent.ini_life - 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_3_lands_full(self):
        return self._land_scene(3, 0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_3_lands_near_full(self):
        return self._land_scene(3, 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_3_lands_injured(self):
        return self._land_scene(3, self.player.opponent.ini_life - 1)

