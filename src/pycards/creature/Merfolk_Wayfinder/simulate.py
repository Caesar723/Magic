from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Merfolk_Wayfinder.model import Merfolk_Wayfinder


@bind_card(Merfolk_Wayfinder)
class Merfolk_Wayfinder_Simulation(Card_Simulation):
    text_parts = {
        "enter.trigger": [
            "When {card_name} enters the battlefield,",
            "Whenever {card_name} enters the battlefield,",
            "When this creature enters the battlefield,",
            "Whenever this creature enters the battlefield,",
            "When {card_name} enters play,",
            "Whenever {card_name} enters play,",
            "When this creature enters play,",
            "Whenever this creature enters play,",
            "When {card_name} comes into play,",
            "Whenever {card_name} comes into play,",
        ],
        "enter.scry": [
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
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _library_scene(self, count, empty_hand=False):
        self.scenario_prepare({"library": {"instant_number": (count, count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)}})
        self.player.library = self.player.library[:count]
        if empty_hand:
            self.player.hand.clear()
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.scry'), 'fields': ('mana_cost',)})
    def simulate_enter_empty(self):
        return self._library_scene(0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.scry'), 'fields': ('mana_cost',)})
    def simulate_enter_one(self):
        return self._library_scene(1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.scry'), 'fields': ('mana_cost',)})
    def simulate_enter_short_scry(self):
        return self._library_scene(max(0, self.card.effect_params["scry_count"] - 1))

    @simulate(evidence={'text': ('enter.trigger', 'enter.scry'), 'fields': ('mana_cost',)})
    def simulate_enter_exact_scry(self):
        return self._library_scene(self.card.effect_params["scry_count"])

    @simulate(evidence={'text': ('enter.trigger', 'enter.scry'), 'fields': ('mana_cost',)})
    def simulate_enter_plenty(self):
        return self._library_scene(self.card.effect_params.get("scry_count", 0) + self.card.effect_params.get("draw_count", 0) + 3)

