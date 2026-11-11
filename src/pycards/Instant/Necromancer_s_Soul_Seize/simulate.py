from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Necromancer_s_Soul_Seize.model import Necromancer_s_Soul_Seize


@bind_card(Necromancer_s_Soul_Seize)
class Necromancer_s_Soul_Seize_Simulation(Card_Simulation):
    scenario_locks={
        '_grave_scene':('self.graveyard', 'self.library'),
    }

    text_parts = {
        "counter.effect": [
            "Counter the creature spell on top of the stack.",
            "Counter the top spell on the stack if it is a creature.",
            "Remove the top creature spell from the stack without resolving it.",
            "Counter the creature spell currently on top of the stack.",
            "Stop the top creature spell on the stack from resolving.",
            "Counter the spell at the top of the stack, restricted to creatures.",
            "Cancel the creature spell at the top of the stack.",
            "Counter the topmost spell on the stack if it is a creature.",
            "Prevent the creature spell on top of the stack from resolving.",
            "Counter the current top spell on the stack, provided it is a creature.",
        ],
        "exile.effect": [
            "If your library is not empty, exile a random card from it.",
            "When a library card is available, choose one at random and move it to exile.",
            "If your library contains a card, exile one of its cards at random.",
            "Exile one randomly chosen card from your library, if any.",
            "If possible, randomly pick a library card and put it into exile.",
            "Choose a library card at random and exile it if one exists.",
            "If any cards remain in your library, move one at random into exile.",
            "Randomly exile one card from your library when it is nonempty.",
            "Take one random card out of your library and put it in exile if available.",
            "If a card can be selected from your library, exile a randomly chosen one.",
        ],
        "return.effect": [
            "If your graveyard has a card of that same broad type, randomly select one, remove it, and add a fresh copy to your hand.",
            "Randomly choose a graveyard card of the same creature, land, sorcery, or instant type if available, remove it, and put a copy into your hand.",
            "If a card of the same broad type is in your graveyard, remove one at random and create a copy in your hand.",
            "Find matching creature, land, sorcery, or instant cards in your graveyard, then remove a random match and add a copy to your hand if any exist.",
            "If the graveyard contains a card with the same broad type, randomly take one out and give yourself a fresh copy in hand.",
            "Choose a graveyard card of the same broad type at random if one is present, remove it, and place a copy in your hand.",
            "If matching creature, land, sorcery, or instant cards exist in your graveyard, remove one randomly and add a copy to your hand.",
            "When a graveyard card of the same broad type is available, remove a random match and create its copy in your hand.",
            "Remove a randomly selected graveyard card of the same broad type, if any, and put a new copy into your hand.",
            "If your graveyard has matching cards of that broad type, pick one at random, remove it, and add a fresh copy to your hand.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack("creature")
        return self.scenario_cast(in_stack=True, provide_mana=False)

    def _grave_scene(self, library_type, grave_type, grave_count, own_target=False, empty_library=False):
        size = grave_count + 3
        self.scenario_prepare({"library": {"instant_number": (size, size), "sorcery_number": (size, size), "creature_number": (size, size), "land_number": (size, size)}})
        cards = list(self.player.library)
        library = [card for card in cards if card.type == library_type]
        self.player.library = [] if empty_library else library[:1]
        self.player.graveyard = [card for card in cards if card.type == grave_type and card not in self.player.library][:grave_count]
        self.scenario_stack("creature", own_target)
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_0_matches_enemy_spell(self):
        return self._grave_scene('Creature', 'Creature', 0, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_0_matches_self_spell(self):
        return self._grave_scene('Creature', 'Creature', 0, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_1_matches_enemy_spell(self):
        return self._grave_scene('Creature', 'Creature', 1, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_1_matches_self_spell(self):
        return self._grave_scene('Creature', 'Creature', 1, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_3_matches_enemy_spell(self):
        return self._grave_scene('Creature', 'Creature', 3, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_3_matches_self_spell(self):
        return self._grave_scene('Creature', 'Creature', 3, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_no_matching_grave_type(self):
        return self._grave_scene('Creature', 'Land', 3)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_land_0_matches_enemy_spell(self):
        return self._grave_scene('Land', 'Land', 0, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_land_0_matches_self_spell(self):
        return self._grave_scene('Land', 'Land', 0, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_land_1_matches_enemy_spell(self):
        return self._grave_scene('Land', 'Land', 1, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_land_1_matches_self_spell(self):
        return self._grave_scene('Land', 'Land', 1, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_land_3_matches_enemy_spell(self):
        return self._grave_scene('Land', 'Land', 3, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_land_3_matches_self_spell(self):
        return self._grave_scene('Land', 'Land', 3, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_land_no_matching_grave_type(self):
        return self._grave_scene('Land', 'Creature', 3)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_sorcery_0_matches_enemy_spell(self):
        return self._grave_scene('Sorcery', 'Sorcery', 0, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_sorcery_0_matches_self_spell(self):
        return self._grave_scene('Sorcery', 'Sorcery', 0, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_sorcery_1_matches_enemy_spell(self):
        return self._grave_scene('Sorcery', 'Sorcery', 1, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_sorcery_1_matches_self_spell(self):
        return self._grave_scene('Sorcery', 'Sorcery', 1, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_sorcery_3_matches_enemy_spell(self):
        return self._grave_scene('Sorcery', 'Sorcery', 3, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_sorcery_3_matches_self_spell(self):
        return self._grave_scene('Sorcery', 'Sorcery', 3, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_sorcery_no_matching_grave_type(self):
        return self._grave_scene('Sorcery', 'Creature', 3)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_instant_0_matches_enemy_spell(self):
        return self._grave_scene('Instant', 'Instant', 0, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_instant_0_matches_self_spell(self):
        return self._grave_scene('Instant', 'Instant', 0, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_instant_1_matches_enemy_spell(self):
        return self._grave_scene('Instant', 'Instant', 1, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_instant_1_matches_self_spell(self):
        return self._grave_scene('Instant', 'Instant', 1, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_instant_3_matches_enemy_spell(self):
        return self._grave_scene('Instant', 'Instant', 3, False)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_instant_3_matches_self_spell(self):
        return self._grave_scene('Instant', 'Instant', 3, True)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_instant_no_matching_grave_type(self):
        return self._grave_scene('Instant', 'Creature', 3)

    @simulate(evidence={'text': ('counter.effect', 'exile.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_library(self):
        return self._grave_scene("Creature", "Creature", 3, empty_library=True)

