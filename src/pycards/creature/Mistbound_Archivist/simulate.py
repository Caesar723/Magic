from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Mistbound_Archivist.model import Mistbound_Archivist


@bind_card(Mistbound_Archivist)
class Mistbound_Archivist_Simulation(Card_Simulation):
    scenario_locks={
        '_library_scene':('self.hand', 'self.library'),
    }

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
        "enter.draw": [
            "Draw {draw_count} card{draw_count_plural}.",
            "Draw {draw_count_word} card{draw_count_plural}.",
            "Take the top {draw_count} card{draw_count_plural} of your library into your hand.",
            "Put the top {draw_count} card{draw_count_plural} from your library into your hand.",
            "Add the top {draw_count} card{draw_count_plural} of your library to your hand.",
            "You draw {draw_count} card{draw_count_plural}.",
            "Draw a total of {draw_count} card{draw_count_plural}.",
            "You draw a total of {draw_count_word} card{draw_count_plural}.",
            "Take {draw_count} card{draw_count_plural} from the top of your library into your hand.",
            "Put {draw_count} card{draw_count_plural} from the top of your library into your hand.",
        ],
        "enter.discard": [
            "Then discard up to {discard_count} cards from your hand at random.",
            "Afterward, randomly discard {discard_count} cards, or all your hand if it is smaller.",
            "Next, discard {discard_count} randomly chosen cards from your hand if available.",
            "You then discard up to {discard_count} cards chosen at random from your hand.",
            "Following the draw, discard {discard_count} cards from your hand at random, taking fewer if necessary.",
            "Then choose and discard {discard_count} cards at random from your hand, or fewer if needed.",
            "After drawing, randomly discard up to {discard_count} hand cards.",
            "Next, remove up to {discard_count} random cards from your hand and put them into your graveyard.",
            "Then put up to {discard_count} randomly chosen hand cards into your graveyard.",
            "Afterward, move up to {discard_count} random cards from your hand to your graveyard.",
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

    @simulate(evidence={'text': ('enter.trigger', 'enter.draw', 'enter.discard'), 'fields': ('mana_cost',)})
    def simulate_enter_empty(self):
        return self._library_scene(0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.draw', 'enter.discard'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_empty_hand(self):
        return self._library_scene(0, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.draw', 'enter.discard'), 'fields': ('mana_cost',)})
    def simulate_enter_one(self):
        return self._library_scene(1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.draw', 'enter.discard'), 'fields': ('mana_cost',)})
    def simulate_enter_one_empty_hand(self):
        return self._library_scene(1, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.draw', 'enter.discard'), 'fields': ('mana_cost',)})
    def simulate_enter_short_draw(self):
        return self._library_scene(max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('enter.trigger', 'enter.draw', 'enter.discard'), 'fields': ('mana_cost',)})
    def simulate_enter_short_draw_empty_hand(self):
        return self._library_scene(max(0, self.card.effect_params["draw_count"] - 1), True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.draw', 'enter.discard'), 'fields': ('mana_cost',)})
    def simulate_enter_exact_draw(self):
        return self._library_scene(self.card.effect_params["draw_count"])

    @simulate(evidence={'text': ('enter.trigger', 'enter.draw', 'enter.discard'), 'fields': ('mana_cost',)})
    def simulate_enter_exact_draw_empty_hand(self):
        return self._library_scene(self.card.effect_params["draw_count"], True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.draw', 'enter.discard'), 'fields': ('mana_cost',)})
    def simulate_enter_plenty(self):
        return self._library_scene(self.card.effect_params.get("scry_count", 0) + self.card.effect_params.get("draw_count", 0) + 3)

    @simulate(evidence={'text': ('enter.trigger', 'enter.draw', 'enter.discard'), 'fields': ('mana_cost',)})
    def simulate_enter_plenty_empty_hand(self):
        return self._library_scene(self.card.effect_params.get("scry_count", 0) + self.card.effect_params.get("draw_count", 0) + 3, True)

