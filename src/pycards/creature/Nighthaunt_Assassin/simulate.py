from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Nighthaunt_Assassin.model import Nighthaunt_Assassin


@bind_card(Nighthaunt_Assassin)
class Nighthaunt_Assassin_Simulation(Card_Simulation):
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
        "enter.effect": [
            "Destroy one random opposing creature with total mana value at most {mana_threshold}, if any are available.",
            "Randomly destroy an opposing creature whose total mana value is {mana_threshold} or less, if present.",
            "Choose an opposing creature with mana value no greater than {mana_threshold} at random and destroy it.",
            "If available, destroy a random creature your opponent controls with mana value of at most {mana_threshold}.",
            "Randomly select and destroy an opposing creature with total mana cost no higher than {mana_threshold}.",
            "Destroy a randomly chosen opposing creature with mana value equal to or below {mana_threshold}, if one exists.",
            "Pick one opposing creature with total mana cost {mana_threshold} or less at random to destroy.",
            "If your opponent has any creatures with mana value at most {mana_threshold}, destroy one randomly.",
            "From opposing creatures costing {mana_threshold} mana or less in total, destroy one chosen at random.",
            "Randomly destroy one available opposing creature whose mana value does not exceed {mana_threshold}.",
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

    def _enter_group(self, count, offset=0, colored=False, missing=1):
        self.scenario_prepare()
        self.player.life = max(1, self.player.ini_life - missing)
        for index in range(count):
            owner = self.player.opponent
            creature = self.scenario_creature(owner, power=index + 1, health=max(1, self.card.effect_params.get("damage", 2) + offset + index), flags={"Hexproof": True})
            cost = self.card.effect_params.get("mana_threshold", 2) + offset + index
            creature.mana_cost = "W" * max(0, cost) if colored else str(max(0, cost))
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_count_0_below(self):
        return self._enter_group(0, offset=-1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_count_0_equal(self):
        return self._enter_group(0, offset=0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_count_0_above(self):
        return self._enter_group(0, offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_count_1_below(self):
        return self._enter_group(1, offset=-1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_count_1_equal(self):
        return self._enter_group(1, offset=0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_count_1_above(self):
        return self._enter_group(1, offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_count_3_below(self):
        return self._enter_group(3, offset=-1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_count_3_equal(self):
        return self._enter_group(3, offset=0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_count_3_above(self):
        return self._enter_group(3, offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_colored_cost(self):
        return self._enter_group(3, colored=True)

