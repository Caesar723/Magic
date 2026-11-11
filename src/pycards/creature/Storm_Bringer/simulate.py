from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Storm_Bringer.model import Storm_Bringer


@bind_card(Storm_Bringer)
class Storm_Bringer_Simulation(Card_Simulation):
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
        "enter.creatures": [
            "{card_name} deals {damage} damage to every opposing creature.",
            "deal {damage} damage to each opposing creature your opponent controls.",
            "every opposing creature takes {damage} damage from {card_name}.",
            "inflict {damage} damage on all opposing creatures.",
            "deal {damage} damage to all opposing creatures your opponent controls.",
            "{card_name} hits each opposing creature for {damage} damage.",
            "each opposing creature is dealt {damage} damage.",
            "{card_name} deals {damage} damage to all opposing creatures in play.",
            "deal an amount of damage equal to {damage} to each opposing creature.",
            "all opposing creatures take {damage} damage each.",
        ],
        "enter.player": [
            "it deals {damage} damage to your opponent.",
            "{card_name} deals {damage} damage to your opponent.",
            "this creature deals {damage} damage to your opponent.",
            "it deals {damage} damage to the opposing player.",
            "{card_name} deals {damage} damage to the opposing player.",
            "this creature deals {damage} damage to the opposing player.",
            "it deals {damage} points of damage to your opponent.",
            "{card_name} deals {damage} points of damage to your opponent.",
            "this creature deals {damage} points of damage to your opponent.",
            "it deals an amount of damage equal to {damage} to your opponent.",
        ],
        "enter.heal": [
            "you gain {heal} life.",
            "gain {heal} life.",
            "you gain a total of {heal} life.",
            "gain a total of {heal} life.",
            "increase your life total by {heal}.",
            "you increase your life total by {heal}.",
            "restore {heal} life.",
            "you restore {heal} life.",
            "gain an amount of life equal to {heal}.",
            "you gain an amount of life equal to {heal}.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
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

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_block_flying_creature(self):
        return self.scenario_combat(True, False, False, enemy_flags={"flying": True})

    def _sweep_scene(self, count, missing_life, enemy_offset):
        self.scenario_prepare()
        damage = self.card.effect_params["damage"]
        self.player.life = max(1, self.player.ini_life - missing_life)
        life = damage + enemy_offset
        if not 1 <= life <= self.player.opponent.ini_life:
            return self.scenario_skip()
        self.player.opponent.life = life
        self.scenario_creature(self.player, power=1, health=damage + 1, flags={})
        for index in range(count):
            self.scenario_creature(self.player.opponent, power=1, health=max(1, damage + index - 1), flags={})
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_full_life_below_lethal(self):
        return self._sweep_scene(0, 0, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_full_life_equal_lethal(self):
        return self._sweep_scene(0, 0, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_full_life_above_lethal(self):
        return self._sweep_scene(0, 0, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_near_full_life_below_lethal(self):
        return self._sweep_scene(0, 1, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_near_full_life_equal_lethal(self):
        return self._sweep_scene(0, 1, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_near_full_life_above_lethal(self):
        return self._sweep_scene(0, 1, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_exact_heal_below_lethal(self):
        return self._sweep_scene(0, self.card.effect_params["heal"], -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_exact_heal_equal_lethal(self):
        return self._sweep_scene(0, self.card.effect_params["heal"], 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_exact_heal_above_lethal(self):
        return self._sweep_scene(0, self.card.effect_params["heal"], 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_injured_below_lethal(self):
        return self._sweep_scene(0, self.player.ini_life - 1, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_injured_equal_lethal(self):
        return self._sweep_scene(0, self.player.ini_life - 1, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_0_enemies_injured_above_lethal(self):
        return self._sweep_scene(0, self.player.ini_life - 1, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_full_life_below_lethal(self):
        return self._sweep_scene(1, 0, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_full_life_equal_lethal(self):
        return self._sweep_scene(1, 0, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_full_life_above_lethal(self):
        return self._sweep_scene(1, 0, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_near_full_life_below_lethal(self):
        return self._sweep_scene(1, 1, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_near_full_life_equal_lethal(self):
        return self._sweep_scene(1, 1, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_near_full_life_above_lethal(self):
        return self._sweep_scene(1, 1, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_exact_heal_below_lethal(self):
        return self._sweep_scene(1, self.card.effect_params["heal"], -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_exact_heal_equal_lethal(self):
        return self._sweep_scene(1, self.card.effect_params["heal"], 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_exact_heal_above_lethal(self):
        return self._sweep_scene(1, self.card.effect_params["heal"], 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_injured_below_lethal(self):
        return self._sweep_scene(1, self.player.ini_life - 1, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_injured_equal_lethal(self):
        return self._sweep_scene(1, self.player.ini_life - 1, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_1_enemies_injured_above_lethal(self):
        return self._sweep_scene(1, self.player.ini_life - 1, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_full_life_below_lethal(self):
        return self._sweep_scene(3, 0, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_full_life_equal_lethal(self):
        return self._sweep_scene(3, 0, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_full_life_above_lethal(self):
        return self._sweep_scene(3, 0, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_near_full_life_below_lethal(self):
        return self._sweep_scene(3, 1, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_near_full_life_equal_lethal(self):
        return self._sweep_scene(3, 1, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_near_full_life_above_lethal(self):
        return self._sweep_scene(3, 1, 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_exact_heal_below_lethal(self):
        return self._sweep_scene(3, self.card.effect_params["heal"], -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_exact_heal_equal_lethal(self):
        return self._sweep_scene(3, self.card.effect_params["heal"], 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_exact_heal_above_lethal(self):
        return self._sweep_scene(3, self.card.effect_params["heal"], 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_injured_below_lethal(self):
        return self._sweep_scene(3, self.player.ini_life - 1, -1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_injured_equal_lethal(self):
        return self._sweep_scene(3, self.player.ini_life - 1, 0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.creatures', 'enter.player', 'enter.heal'), 'fields': ('mana_cost', 'special_type')})
    def simulate_enter_3_enemies_injured_above_lethal(self):
        return self._sweep_scene(3, self.player.ini_life - 1, 1)

