from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Arcane_Inferno.model import Arcane_Inferno


@bind_card(Arcane_Inferno)
class Arcane_Inferno_Simulation(Card_Simulation):
    scenario_locks={
        '_damage_scene':('opponent.battlefield', 'self.battlefield', 'self.land_area'),
    }

    text_parts = {
        "damage.base": [
            "{card_name} deals {damage} damage to a target creature or player.",
            "Deal {damage} damage to a chosen creature or player.",
            "Target creature or player takes {damage} damage from {card_name}.",
            "{card_name} inflicts {damage} damage on a target creature or player.",
            "Choose a creature or player and deal {damage} damage to it.",
            "Hit a target creature or player for {damage} damage.",
            "A creature or player of your choice is dealt {damage} damage.",
            "{card_name} deals {damage} damage to the creature or player you target.",
            "Deal a target creature or player an amount of damage equal to {damage}.",
            "Target a creature or player to be dealt {damage} damage by {card_name}.",
        ],
        "damage.condition": [
            "If you control a creature with power at least {power_threshold},",
            "If any creature you control has power {power_threshold} or greater,",
            "When your battlefield contains a creature with power no lower than {power_threshold},",
            "If a creature on your battlefield has at least {power_threshold} power,",
            "If you have a creature whose power is {power_threshold} or more,",
            "When one or more creatures you control have power at least {power_threshold},",
            "If any of your creatures has {power_threshold} or more power,",
            "If your side includes a creature with power of at least {power_threshold},",
            "If you control at least one creature whose power is {power_threshold} or higher,",
            "When a creature under your control has power equal to or above {power_threshold},",
        ],
        "damage.high": [
            "{card_name} deals {damage_high} damage to that target instead.",
            "deal {damage_high} damage to the target instead.",
            "replace the damage with {damage_high} damage to that target.",
            "instead deal {damage_high} damage to the chosen target.",
            "that target takes {damage_high} damage instead.",
            "{card_name} inflicts {damage_high} damage on the target instead.",
            "change the damage dealt to the target to {damage_high}.",
            "the damage to that target becomes {damage_high} instead.",
            "deal an amount of damage equal to {damage_high} to the target instead.",
            "{card_name} hits the target for {damage_high} damage instead.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _damage_scene(self, target_role, life_offset, branch=None, target_flags=None):
        self.scenario_prepare()
        params = self.card.effect_params
        damage = params.get("damage", params.get("damage_low", 0))
        if branch is not None:
            power = max(0, params["power_threshold"] + branch)
            self.scenario_creature(self.player, power=power, health=20, flags={})
            if power >= params["power_threshold"]:
                damage = params["damage_high"]
        life = damage + life_offset
        if life <= 0:
            return self.scenario_skip()
        if target_role in ("self_creature", "enemy_creature"):
            owner = self.player if target_role == "self_creature" else self.player.opponent
            power = 1
            target = self.scenario_creature(owner, power=power, health=life, flags=target_flags or {})
            subaction = (11 if owner is self.player else 1) + owner.battlefield.index(target)
        else:
            owner = self.player if target_role == "self_player" else self.player.opponent
            if life > owner.ini_life:
                return self.scenario_skip()
            owner.life = life
            subaction = 22 if owner is self.player else 21
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast((subaction,), provide_mana=False)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_below_condition_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_below_condition_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_below_condition_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_below_condition_below_lethal(self):
        return self._damage_scene('self_creature', -1, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_below_condition_equal_lethal(self):
        return self._damage_scene('self_creature', 0, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_below_condition_above_lethal(self):
        return self._damage_scene('self_creature', 1, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_below_condition_below_lethal(self):
        return self._damage_scene('enemy_player', -1, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_below_condition_equal_lethal(self):
        return self._damage_scene('enemy_player', 0, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_below_condition_above_lethal(self):
        return self._damage_scene('enemy_player', 1, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_below_condition_below_lethal(self):
        return self._damage_scene('self_player', -1, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_below_condition_equal_lethal(self):
        return self._damage_scene('self_player', 0, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_below_condition_above_lethal(self):
        return self._damage_scene('self_player', 1, branch=-1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_equal_condition_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_equal_condition_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_equal_condition_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_equal_condition_below_lethal(self):
        return self._damage_scene('self_creature', -1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_equal_condition_equal_lethal(self):
        return self._damage_scene('self_creature', 0, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_equal_condition_above_lethal(self):
        return self._damage_scene('self_creature', 1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_equal_condition_below_lethal(self):
        return self._damage_scene('enemy_player', -1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_equal_condition_equal_lethal(self):
        return self._damage_scene('enemy_player', 0, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_equal_condition_above_lethal(self):
        return self._damage_scene('enemy_player', 1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_equal_condition_below_lethal(self):
        return self._damage_scene('self_player', -1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_equal_condition_equal_lethal(self):
        return self._damage_scene('self_player', 0, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_equal_condition_above_lethal(self):
        return self._damage_scene('self_player', 1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_above_condition_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_above_condition_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_above_condition_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_above_condition_below_lethal(self):
        return self._damage_scene('self_creature', -1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_above_condition_equal_lethal(self):
        return self._damage_scene('self_creature', 0, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_above_condition_above_lethal(self):
        return self._damage_scene('self_creature', 1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_above_condition_below_lethal(self):
        return self._damage_scene('enemy_player', -1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_above_condition_equal_lethal(self):
        return self._damage_scene('enemy_player', 0, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_above_condition_above_lethal(self):
        return self._damage_scene('enemy_player', 1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_above_condition_below_lethal(self):
        return self._damage_scene('self_player', -1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_above_condition_equal_lethal(self):
        return self._damage_scene('self_player', 0, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_above_condition_above_lethal(self):
        return self._damage_scene('self_player', 1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_empty_board_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_empty_board_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_empty_board_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_empty_board_below_lethal(self):
        return self._damage_scene('self_creature', -1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_empty_board_equal_lethal(self):
        return self._damage_scene('self_creature', 0, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_empty_board_above_lethal(self):
        return self._damage_scene('self_creature', 1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_empty_board_below_lethal(self):
        return self._damage_scene('enemy_player', -1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_empty_board_equal_lethal(self):
        return self._damage_scene('enemy_player', 0, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_empty_board_above_lethal(self):
        return self._damage_scene('enemy_player', 1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_empty_board_below_lethal(self):
        return self._damage_scene('self_player', -1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_empty_board_equal_lethal(self):
        return self._damage_scene('self_player', 0, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_empty_board_above_lethal(self):
        return self._damage_scene('self_player', 1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_hexproof_target(self):
        return self._damage_scene("enemy_creature", 1, branch=None, target_flags={"Hexproof": True})

