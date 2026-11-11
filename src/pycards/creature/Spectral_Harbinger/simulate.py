from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Spectral_Harbinger.model import Spectral_Harbinger


@bind_card(Spectral_Harbinger)
class Spectral_Harbinger_Simulation(Card_Simulation):
    text_parts = {
        "keyword.flying": [
            "Flying.",
            "This creature has flying.",
            "{card_name} has flying.",
            "This creature has the flying ability.",
            "{card_name} has the flying ability.",
            "Flying (Only creatures with flying or reach can block this creature).",
            "This creature can be blocked only by creatures with flying or reach.",
            "Only creatures with flying or reach can block this creature.",
            "Creatures without flying or reach cannot block this creature.",
            "This creature has flying. Creatures without flying or reach cannot block it.",
        ],
        "keyword.lifelink": [
            "Lifelink.",
            "This creature has lifelink.",
            "{card_name} has lifelink.",
            "This creature has the lifelink ability.",
            "{card_name} has the lifelink ability.",
            "Lifelink (Damage dealt by this creature also causes you to gain that much life).",
            "Damage dealt by this creature also causes you to gain that much life.",
            "Damage dealt by {card_name} also causes you to gain that much life.",
            "This creature has lifelink, so its damage also causes you to gain that much life.",
            "{card_name} has lifelink, so its damage also causes you to gain that much life.",
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
        "enter.effect": [
            "Remove one random creature from your graveyard, if available, then gain {heal} life.",
            "If your graveyard contains a creature, randomly remove one and gain {heal} life.",
            "Randomly take one creature card out of your graveyard and gain {heal} life, if possible.",
            "Choose a random creature in your graveyard to remove, then restore {heal} life.",
            "Gain {heal} life after removing a randomly chosen creature from your graveyard, if any are available.",
            "If you have a graveyard creature, remove one at random and restore {heal} life.",
            "Remove one randomly selected creature card from your graveyard to gain {heal} life.",
            "When your graveyard has any creatures, randomly remove one and increase your life by {heal}.",
            "Take a random creature out of your graveyard, if present, and then gain {heal} life.",
            "If available, remove a random graveyard creature of yours and gain {heal} life afterward.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_block_flying_creature(self):
        return self.scenario_combat(True, False, False, enemy_flags={"flying": True})

    def _enter_group(self, count, offset=0, colored=False, missing=1):
        self.scenario_prepare()
        self.player.life = max(1, self.player.ini_life - missing)
        self.player.graveyard.clear()
        for index in range(count):
            owner = self.player
            creature = self.scenario_creature(owner, power=index + 1, health=max(1, self.card.effect_params.get("damage", 2) + offset + index), flags={"Hexproof": True})
            cost = self.card.effect_params.get("mana_threshold", 2) + offset + index
            creature.mana_cost = "W" * max(0, cost) if colored else str(max(0, cost))
            owner.remove_card(creature, "battlefield")
            owner.append_card(creature, "graveyard")
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
    def simulate_enter_heal_full(self):
        return self._enter_group(2, missing=0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_heal_near_full(self):
        return self._enter_group(2, missing=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_heal_injured(self):
        return self._enter_group(2, missing=self.player.ini_life - 1)

