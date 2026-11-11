from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Kothar_the_Soul_Reaper.model import Kothar_the_Soul_Reaper


@bind_card(Kothar_the_Soul_Reaper)
class Kothar_the_Soul_Reaper_Simulation(Card_Simulation):
    scenario_locks={
        '_simulate_enter':('opponent.battlefield',),
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
        "enter.effect": [
            "destroy a random creature your opponent controls, if any.",
            "if your opponent controls a creature, destroy one of them chosen at random.",
            "randomly choose one opposing creature and destroy it, if one is available.",
            "destroy one randomly chosen creature on the opposing battlefield, if possible.",
            "choose a creature at random from your opponent's battlefield and destroy it if any exist.",
            "destroy one of your opponent's creatures at random when there is one.",
            "if an opposing creature is present, destroy a randomly selected one.",
            "destroy a creature chosen randomly from those your opponent controls, if available.",
            "if your opponent has any creatures in play, randomly select and destroy one.",
            "randomly select one creature controlled by your opponent and destroy it, if possible.",
        ],
        "death.trigger": [
            "Whenever another creature dies while {card_name} remains on the battlefield,",
            "When another creature dies and {card_name} is still on the battlefield,",
            "Each time another creature dies while this creature stays on the battlefield,",
            "Whenever a different creature dies while this creature remains in play,",
            "When another creature dies while {card_name} is in play,",
            "Each time a different creature dies and {card_name} remains in play,",
            "Whenever another creature dies with {card_name} still on the battlefield,",
            "When a different creature dies with this creature still in play,",
            "Every time another creature dies while {card_name} stays on the battlefield,",
            "Whenever another creature dies while this creature is still on the battlefield,",
        ],
        "death.effect": [
            "{card_name} gets +{power_bonus}/+{toughness_bonus}.",
            "this creature gets +{power_bonus}/+{toughness_bonus}.",
            "give {card_name} +{power_bonus}/+{toughness_bonus}.",
            "give this creature +{power_bonus}/+{toughness_bonus}.",
            "{card_name} gains +{power_bonus}/+{toughness_bonus}.",
            "this creature gains +{power_bonus}/+{toughness_bonus}.",
            "increase this creature's power by {power_bonus} and toughness by {toughness_bonus}.",
            "increase {card_name}'s power by {power_bonus} and toughness by {toughness_bonus}.",
            "add {power_bonus} to this creature's power and {toughness_bonus} to its toughness.",
            "add {power_bonus} to {card_name}'s power and {toughness_bonus} to its toughness.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('death.trigger', 'death.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('death.trigger', 'death.effect'), 'fields': ('attack', 'defend', 'special_type')})
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

    @simulate(evidence={'text': ('death.trigger', 'death.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'text': ('death.trigger', 'death.effect'), 'fields': ('attack', 'defend', 'special_type')})
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

    def _simulate_enter(self, count):
        self.scenario_prepare()
        for _ in range(count):
            self.scenario_creature(self.player.opponent, flags={})
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_0_creatures(self):
        return self._simulate_enter(0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect', 'death.trigger', 'death.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_1_creatures(self):
        return self._simulate_enter(1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect', 'death.trigger', 'death.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_3_creatures(self):
        return self._simulate_enter(3)

