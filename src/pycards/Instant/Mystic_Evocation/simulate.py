from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Mystic_Evocation.model import Mystic_Evocation


@bind_card(Mystic_Evocation)
class Mystic_Evocation_Simulation(Card_Simulation):
    text_parts = {
        "counter.effect": [
            "Counter the instant, sorcery, or land spell on top of the stack.",
            "Counter the top spell on the stack if it is an instant, sorcery, or land.",
            "Remove the top instant, sorcery, or land spell from the stack without resolving it.",
            "Counter the instant, sorcery, or land spell currently on top of the stack.",
            "Stop the top instant, sorcery, or land spell on the stack from resolving.",
            "Counter the spell at the top of the stack, restricted to instants, sorceries, and lands.",
            "Cancel the instant, sorcery, or land spell at the top of the stack.",
            "Counter the topmost spell on the stack if it is an instant, sorcery, or land.",
            "Prevent the instant, sorcery, or land spell on top of the stack from resolving.",
            "Counter the current top spell on the stack, provided it is an instant, sorcery, or land.",
        ],
        "scry.effect": [
            "look at up to the top {scry_count} cards of your library, keep any of them on top in their existing order, and move the rest to the bottom in their existing order.",
            "examine the top {scry_count} cards of your library or fewer if necessary, keep any on top in order, and put the others on the bottom in order.",
            "inspect up to {scry_count} cards from the top of your library, leaving chosen cards on top and moving the unchosen cards to the bottom without reordering either group.",
            "look at the first {scry_count} available library cards, choose which to keep on top, and put the rest on the bottom while preserving each group's order.",
            "examine up to the first {scry_count} cards of your library, retaining any on top and moving the others to the bottom in their current order.",
            "look through up to the top {scry_count} library cards, leave any chosen cards on top in order, and place the remaining cards at the bottom in order.",
            "inspect the top {scry_count} cards of your library or all of it if smaller, keep any on top, and move the rest to the bottom without changing their relative order.",
            "view up to {scry_count} cards from the top of your library, keep your chosen cards there, and place the rest at the bottom while maintaining both groups' order.",
            "examine at most the top {scry_count} library cards, retaining any chosen cards in place and moving all remaining examined cards to the bottom in order.",
            "look at up to {scry_count} cards from the top, keep any of them there in their current order, and put the remaining examined cards at the bottom in their current order.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    def _scry_scene(self, target_type, count, own_target=False):
        self.scenario_prepare({"library": {"instant_number": (count, count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)}})
        self.player.library = [card for card in self.player.library if card.type == "Instant"][:count]
        self.scenario_stack(target_type, own_target, cost=0 if target_type == "land" else 3)
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_empty(self):
        return self._scry_scene('instant', 0, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_empty(self):
        return self._scry_scene('instant', 0, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_one(self):
        return self._scry_scene('instant', 1, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_one(self):
        return self._scry_scene('instant', 1, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_short(self):
        return self._scry_scene('instant', max(0, self.card.effect_params["scry_count"] - 1), False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_short(self):
        return self._scry_scene('instant', max(0, self.card.effect_params["scry_count"] - 1), True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_exact(self):
        return self._scry_scene('instant', self.card.effect_params["scry_count"], False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_exact(self):
        return self._scry_scene('instant', self.card.effect_params["scry_count"], True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_plenty(self):
        return self._scry_scene('instant', self.card.effect_params["scry_count"] + 2, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_plenty(self):
        return self._scry_scene('instant', self.card.effect_params["scry_count"] + 2, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_empty(self):
        return self._scry_scene('sorcery', 0, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_empty(self):
        return self._scry_scene('sorcery', 0, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_one(self):
        return self._scry_scene('sorcery', 1, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_one(self):
        return self._scry_scene('sorcery', 1, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_short(self):
        return self._scry_scene('sorcery', max(0, self.card.effect_params["scry_count"] - 1), False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_short(self):
        return self._scry_scene('sorcery', max(0, self.card.effect_params["scry_count"] - 1), True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_exact(self):
        return self._scry_scene('sorcery', self.card.effect_params["scry_count"], False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_exact(self):
        return self._scry_scene('sorcery', self.card.effect_params["scry_count"], True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_plenty(self):
        return self._scry_scene('sorcery', self.card.effect_params["scry_count"] + 2, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_plenty(self):
        return self._scry_scene('sorcery', self.card.effect_params["scry_count"] + 2, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_land_empty(self):
        return self._scry_scene('land', 0, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_land_empty(self):
        return self._scry_scene('land', 0, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_land_one(self):
        return self._scry_scene('land', 1, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_land_one(self):
        return self._scry_scene('land', 1, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_land_short(self):
        return self._scry_scene('land', max(0, self.card.effect_params["scry_count"] - 1), False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_land_short(self):
        return self._scry_scene('land', max(0, self.card.effect_params["scry_count"] - 1), True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_land_exact(self):
        return self._scry_scene('land', self.card.effect_params["scry_count"], False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_land_exact(self):
        return self._scry_scene('land', self.card.effect_params["scry_count"], True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_land_plenty(self):
        return self._scry_scene('land', self.card.effect_params["scry_count"] + 2, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_land_plenty(self):
        return self._scry_scene('land', self.card.effect_params["scry_count"] + 2, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_empty(self):
        return self._scry_scene('creature', 0, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_empty(self):
        return self._scry_scene('creature', 0, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_one(self):
        return self._scry_scene('creature', 1, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_one(self):
        return self._scry_scene('creature', 1, True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_short(self):
        return self._scry_scene('creature', max(0, self.card.effect_params["scry_count"] - 1), False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_short(self):
        return self._scry_scene('creature', max(0, self.card.effect_params["scry_count"] - 1), True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_exact(self):
        return self._scry_scene('creature', self.card.effect_params["scry_count"], False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_exact(self):
        return self._scry_scene('creature', self.card.effect_params["scry_count"], True)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_plenty(self):
        return self._scry_scene('creature', self.card.effect_params["scry_count"] + 2, False)

    @simulate(evidence={'text': ('counter.effect', 'scry.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_plenty(self):
        return self._scry_scene('creature', self.card.effect_params["scry_count"] + 2, True)

