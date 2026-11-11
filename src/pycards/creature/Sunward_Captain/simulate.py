from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Sunward_Captain.model import Sunward_Captain


@bind_card(Sunward_Captain)
class Sunward_Captain_Simulation(Card_Simulation):
    scenario_locks={
        '_token_scene':('self.battlefield',),
    }

    text_parts = {
        "keyword.vigilance": [
            "Vigilance.",
            "This creature has vigilance.",
            "{card_name} has vigilance.",
            "This creature has the vigilance ability.",
            "{card_name} has the vigilance ability.",
            "Attacking does not cause this creature to tap.",
            "This creature does not tap when it attacks.",
            "{card_name} does not tap when it attacks.",
            "Vigilance (Attacking does not cause this creature to tap).",
            "This creature has vigilance and does not tap when it attacks.",
        ],
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
        "enter.tokens": [
            "create {token_count} {token_power}/{token_toughness} white Soldier creature token{token_count_plural}.",
            "put {token_count} {token_power}/{token_toughness} white Soldier creature token{token_count_plural} onto the battlefield.",
            "summon {token_count} white {token_power}/{token_toughness} Soldier creature token{token_count_plural}.",
            "create {token_count_word} white Soldier creature token{token_count_plural} with power {token_power} and toughness {token_toughness}.",
            "create {token_count_word} {token_power}/{token_toughness} white Soldier creature token{token_count_plural} under your control.",
            "put {token_count_word} white {token_power}/{token_toughness} Soldier creature token{token_count_plural} into play.",
            "create a total of {token_count} white Soldier creature token{token_count_plural}, each {token_power}/{token_toughness}.",
            "add {token_count} {token_power}/{token_toughness} white Soldier creature token{token_count_plural} to your battlefield.",
            "bring {token_count_word} white Soldier creature token{token_count_plural} into play with {token_power} power and {token_toughness} toughness each.",
            "create {token_count} Soldier creature token{token_count_plural} that are white and {token_power}/{token_toughness}.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('keyword.vigilance',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.vigilance',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.vigilance',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.vigilance',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.vigilance',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.vigilance',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.vigilance',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.vigilance',), 'fields': ('attack', 'defend', 'special_type')})
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

    @simulate(evidence={'text': ('keyword.vigilance',), 'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'text': ('keyword.vigilance',), 'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _token_scene(self, count, missing_life=0):
        self.scenario_prepare()
        for _ in range(count):
            self.scenario_creature(self.player, flags={})
        self.player.life = max(1, self.player.ini_life - missing_life)
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.tokens'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_board(self):
        return self._token_scene(0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.tokens'), 'fields': ('mana_cost',)})
    def simulate_enter_one_creature(self):
        return self._token_scene(1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.tokens'), 'fields': ('mana_cost',)})
    def simulate_enter_multiple_creatures(self):
        return self._token_scene(3)

    @simulate(evidence={'text': ('enter.trigger', 'enter.tokens'), 'fields': ('mana_cost',)})
    def simulate_enter_fill_visible_board(self):
        return self._token_scene(max(0, 9 - self.card.effect_params["token_count"]))

