from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.sorcery.Chaotic_Eruption.model import Chaotic_Eruption


@bind_card(Chaotic_Eruption)
class Chaotic_Eruption_Simulation(Card_Simulation):
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
        "remove.hand": [
            "Remove up to {discard_count} cards from your opponent's hand at random.",
            "Randomly remove {discard_count} opposing hand cards, or all of them if fewer are available.",
            "Take up to {discard_count} random cards out of your opponent's hand.",
            "Your opponent loses up to {discard_count} random cards from their hand.",
            "Remove up to {discard_count} randomly selected cards from your opponent's hand.",
            "Choose and remove up to {discard_count} cards at random from the opposing hand.",
            "Randomly take up to {discard_count} opposing hand cards out of that hand.",
            "Take up to {discard_count} cards chosen at random out of the opponent's hand.",
            "Remove {discard_count} randomly chosen opposing hand cards if that many are available, or all of them otherwise.",
            "Your opponent has up to {discard_count} randomly chosen hand cards removed.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _land_scene(self, count, missing=1, hand_count=3):
        self.scenario_prepare()
        self.room.env_mana(self.player.opponent, {"W": (count, count)})
        self.player.opponent.life = max(1, self.player.opponent.ini_life - missing)
        self.room.env_initinal_hand(self.player.opponent, {"instant_number": (hand_count, hand_count), "creature_number": (0, 0), "sorcery_number": (0, 0), "land_number": (0, 0)})
        return self.scenario_cast((1,))

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_0_lands_full(self):
        return self._land_scene(0, 0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_0_lands_near_full(self):
        return self._land_scene(0, 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_0_lands_injured(self):
        return self._land_scene(0, self.player.opponent.ini_life - 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_1_lands_full(self):
        return self._land_scene(1, 0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_1_lands_near_full(self):
        return self._land_scene(1, 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_1_lands_injured(self):
        return self._land_scene(1, self.player.opponent.ini_life - 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_3_lands_full(self):
        return self._land_scene(3, 0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_3_lands_near_full(self):
        return self._land_scene(3, 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_3_lands_injured(self):
        return self._land_scene(3, self.player.opponent.ini_life - 1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_hand_empty(self):
        return self._land_scene(1, hand_count=0)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_hand_one(self):
        return self._land_scene(1, hand_count=1)

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_hand_exact(self):
        return self._land_scene(1, hand_count=self.card.effect_params["discard_count"])

    @simulate(evidence={'text': ('target.scope', 'remove.effect', 'remove.hand'), 'fields': ('mana_cost',)})
    def simulate_hand_plenty(self):
        return self._land_scene(1, hand_count=self.card.effect_params["discard_count"] + 2)

