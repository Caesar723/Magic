from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Dreamweaver_Archivist.model import Dreamweaver_Archivist


@bind_card(Dreamweaver_Archivist)
class Dreamweaver_Archivist_Simulation(Card_Simulation):
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
        "enter.option": [
            "you may use this optional ability.",
            "you may choose to use the following ability.",
            "you can choose whether to use this ability.",
            "you may opt to perform the following effect.",
            "you have the choice to use the following effect.",
            "you may choose to perform this optional effect.",
            "you can opt into the following effect.",
            "you may use the following effect or do nothing.",
            "you can choose this ability or decline it.",
            "you may accept or decline the following effect.",
        ],
        "enter.remove": [
            "If you do, remove up to {discard_count} random cards from your hand.",
            "If chosen, first remove up to {discard_count} cards at random from your hand.",
            "On accepting, randomly remove {discard_count} hand cards or all of them if fewer are available.",
            "If you accept, remove up to {discard_count} randomly chosen cards from your hand.",
            "If used, take up to {discard_count} random cards out of your hand first.",
            "If selected, remove up to {discard_count} cards chosen at random from your hand.",
            "If you use it, first remove up to {discard_count} random hand cards.",
            "If you choose this effect, randomly remove up to {discard_count} cards from your hand.",
            "If accepted, take up to {discard_count} randomly selected cards out of your hand.",
            "If you opt in, remove up to {discard_count} hand cards chosen randomly.",
        ],
        "enter.draw": [
            "Then draw {draw_count} card{draw_count_plural}.",
            "Then draw {draw_count_word} card{draw_count_plural}.",
            "Then take the top {draw_count} card{draw_count_plural} of your library into your hand.",
            "Then put the top {draw_count} card{draw_count_plural} from your library into your hand.",
            "Then add the top {draw_count} card{draw_count_plural} of your library to your hand.",
            "Then you draw {draw_count} card{draw_count_plural}.",
            "Then draw a total of {draw_count} card{draw_count_plural}.",
            "Then you draw a total of {draw_count_word} card{draw_count_plural}.",
            "Then take {draw_count} card{draw_count_plural} from the top of your library into your hand.",
            "Then put {draw_count} card{draw_count_plural} from the top of your library into your hand.",
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

    async def _selection_step(self, player=None, opponent=None, selection_random=False):
        label = "Use ability" if self.selected_option == 1 else "Do nothing"
        return [self.card.create_selection(label, self.selected_option)]

    def _optional_scene(self, count, option, empty_hand):
        self.selected_option = option
        self.card.selection_step = self._selection_step
        return self._library_scene(count, empty_hand)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.remove', 'enter.draw'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_accept_with_hand(self):
        return self._optional_scene(0, 1, False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.remove', 'enter.draw'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_accept_empty_hand(self):
        return self._optional_scene(0, 1, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_decline_with_hand(self):
        return self._optional_scene(0, 2, False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_decline_empty_hand(self):
        return self._optional_scene(0, 2, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.remove', 'enter.draw'), 'fields': ('mana_cost',)})
    def simulate_enter_one_accept_with_hand(self):
        return self._optional_scene(1, 1, False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.remove', 'enter.draw'), 'fields': ('mana_cost',)})
    def simulate_enter_one_accept_empty_hand(self):
        return self._optional_scene(1, 1, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_one_decline_with_hand(self):
        return self._optional_scene(1, 2, False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_one_decline_empty_hand(self):
        return self._optional_scene(1, 2, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.remove', 'enter.draw'), 'fields': ('mana_cost',)})
    def simulate_enter_short_draw_accept_with_hand(self):
        return self._optional_scene(max(0, self.card.effect_params["draw_count"] - 1), 1, False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.remove', 'enter.draw'), 'fields': ('mana_cost',)})
    def simulate_enter_short_draw_accept_empty_hand(self):
        return self._optional_scene(max(0, self.card.effect_params["draw_count"] - 1), 1, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_short_draw_decline_with_hand(self):
        return self._optional_scene(max(0, self.card.effect_params["draw_count"] - 1), 2, False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_short_draw_decline_empty_hand(self):
        return self._optional_scene(max(0, self.card.effect_params["draw_count"] - 1), 2, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.remove', 'enter.draw'), 'fields': ('mana_cost',)})
    def simulate_enter_exact_draw_accept_with_hand(self):
        return self._optional_scene(self.card.effect_params["draw_count"], 1, False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.remove', 'enter.draw'), 'fields': ('mana_cost',)})
    def simulate_enter_exact_draw_accept_empty_hand(self):
        return self._optional_scene(self.card.effect_params["draw_count"], 1, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_exact_draw_decline_with_hand(self):
        return self._optional_scene(self.card.effect_params["draw_count"], 2, False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_exact_draw_decline_empty_hand(self):
        return self._optional_scene(self.card.effect_params["draw_count"], 2, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.remove', 'enter.draw'), 'fields': ('mana_cost',)})
    def simulate_enter_plenty_accept_with_hand(self):
        return self._optional_scene(self.card.effect_params.get("scry_count", 0) + self.card.effect_params.get("draw_count", 0) + 3, 1, False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.remove', 'enter.draw'), 'fields': ('mana_cost',)})
    def simulate_enter_plenty_accept_empty_hand(self):
        return self._optional_scene(self.card.effect_params.get("scry_count", 0) + self.card.effect_params.get("draw_count", 0) + 3, 1, True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_plenty_decline_with_hand(self):
        return self._optional_scene(self.card.effect_params.get("scry_count", 0) + self.card.effect_params.get("draw_count", 0) + 3, 2, False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_plenty_decline_empty_hand(self):
        return self._optional_scene(self.card.effect_params.get("scry_count", 0) + self.card.effect_params.get("draw_count", 0) + 3, 2, True)

