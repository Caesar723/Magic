from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Emberheart_Salamander.model import Emberheart_Salamander


@bind_card(Emberheart_Salamander)
class Emberheart_Salamander_Simulation(Card_Simulation):
    text_parts = {
        "keyword.trample": [
            "Trample.",
            "This creature has trample.",
            "{card_name} has trample.",
            "This creature has the trample ability.",
            "{card_name} has the trample ability.",
            "Trample (This creature can deal excess combat damage to the defending player).",
            "This creature has trample and can deal excess combat damage to the defending player.",
            "{card_name} has trample and can deal excess combat damage to the defending player.",
            "This creature can deal excess combat damage to the defending player through trample.",
            "{card_name} can deal excess combat damage to the defending player through trample.",
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
            "{card_name} deals {damage} damage to the target.",
            "Deal {damage} damage to the selected target.",
            "The target takes {damage} damage from {card_name}.",
            "{card_name} inflicts {damage} damage on that target.",
            "Deal the chosen target {damage} damage.",
            "Hit the target for {damage} damage.",
            "The selected target is dealt {damage} damage.",
            "Deal an amount of damage equal to {damage} to the target.",
            "{card_name} hits the chosen target for {damage} damage.",
            "Inflict {damage} points of damage on the target.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('keyword.trample',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.trample',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.trample',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.trample',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.trample',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.trample',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.trample',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.trample',), 'fields': ('attack', 'defend', 'special_type')})
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

    def _enter_scene(self, role, offset=1, extra_red=1, option=1, hand_count=1, hexproof=False, power_offset=0, in_stack=False):
        self.scenario_prepare()
        self.player.hand.clear()
        for _ in range(hand_count):
            self.player.append_card(self.card.copy_for_player(self.player), "hand")
        subaction = 0
        if role in ("self_creature", "enemy_creature"):
            owner = self.player if role == "self_creature" else self.player.opponent
            health = self.card.effect_params.get("damage", 2) + offset
            if health <= 0:
                return self.scenario_skip()
            power = max(0, self.card.effect_params.get("power_threshold", 2) + power_offset)
            self.scenario_creature(owner, power=power, health=health, flags={"Hexproof": hexproof})
            subaction = 11 if owner is self.player else 1
        elif role in ("self_player", "enemy_player"):
            owner = self.player if role == "self_player" else self.player.opponent
            life = self.card.effect_params.get("damage", 2) + offset
            if not 1 <= life <= owner.ini_life:
                return self.scenario_skip()
            owner.life = life
            subaction = 22 if owner is self.player else 21
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast((subaction,), provide_mana=False, in_stack=in_stack)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_creature_overkill(self):
        return self._enter_scene('self_creature', offset=-1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_creature_equal(self):
        return self._enter_scene('self_creature', offset=0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_creature_survives(self):
        return self._enter_scene('self_creature', offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_creature_overkill(self):
        return self._enter_scene('enemy_creature', offset=-1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_creature_equal(self):
        return self._enter_scene('enemy_creature', offset=0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_creature_survives(self):
        return self._enter_scene('enemy_creature', offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_player_overkill(self):
        return self._enter_scene('self_player', offset=-1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_player_equal(self):
        return self._enter_scene('self_player', offset=0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_player_survives(self):
        return self._enter_scene('self_player', offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_player_overkill(self):
        return self._enter_scene('enemy_player', offset=-1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_player_equal(self):
        return self._enter_scene('enemy_player', offset=0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_player_survives(self):
        return self._enter_scene('enemy_player', offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_none_normal(self):
        return self._enter_scene('none', offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_self_creature_hexproof(self):
        return self._enter_scene('self_creature', hexproof=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_creature_hexproof(self):
        return self._enter_scene('enemy_creature', hexproof=True)

