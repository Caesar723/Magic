from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Flames_of_Fury.model import Flames_of_Fury
from pycards.land.Mountain.model import Mountain


@bind_card(Flames_of_Fury)
class Flames_of_Fury_Simulation(Card_Simulation):
    scenario_locks={
        '_damage_scene':('opponent.land_area', 'self.land_area'),
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
            "If you control a land named Mountain,",
            "If a land named Mountain is on your battlefield,",
            "When you have a land whose name is Mountain,",
            "If at least one land named Mountain is under your control,",
            "If your land area contains a land named Mountain,",
            "When a land named Mountain is both under your control,",
            "If there is a land named Mountain among your lands,",
            "If one or more lands named Mountain are on your side,",
            "When your lands include a land named Mountain,",
            "If a land you control is named Mountain,",
        ],
        "damage.high": [
            "it deals {damage_bonus} additional damage to the target.",
            "increase the damage to that target by {damage_bonus}.",
            "add {damage_bonus} to the damage dealt to the target.",
            "deal an extra {damage_bonus} damage to the target.",
            "it deals {damage_bonus} more damage to the chosen target.",
            "raise the damage to the target by {damage_bonus}.",
            "the target takes an additional {damage_bonus} damage.",
            "add an extra {damage_bonus} damage to that target.",
            "increase the damage amount by {damage_bonus}.",
            "{card_name} deals {damage_bonus} extra damage to the target.",
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
            mountain = Mountain(self.player)
            mountain.flag_dict["tap"] = branch == 0
            self.stage_card(mountain, zone="land_area")
            damage += params["damage_bonus"]
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
    def simulate_enemy_creature_no_mountain_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_no_mountain_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_no_mountain_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_no_mountain_below_lethal(self):
        return self._damage_scene('self_creature', -1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_no_mountain_equal_lethal(self):
        return self._damage_scene('self_creature', 0, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_no_mountain_above_lethal(self):
        return self._damage_scene('self_creature', 1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_no_mountain_below_lethal(self):
        return self._damage_scene('enemy_player', -1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_no_mountain_equal_lethal(self):
        return self._damage_scene('enemy_player', 0, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_no_mountain_above_lethal(self):
        return self._damage_scene('enemy_player', 1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_no_mountain_below_lethal(self):
        return self._damage_scene('self_player', -1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_no_mountain_equal_lethal(self):
        return self._damage_scene('self_player', 0, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_no_mountain_above_lethal(self):
        return self._damage_scene('self_player', 1, branch=None)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_tapped_mountain_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_tapped_mountain_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_tapped_mountain_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_tapped_mountain_below_lethal(self):
        return self._damage_scene('self_creature', -1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_tapped_mountain_equal_lethal(self):
        return self._damage_scene('self_creature', 0, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_tapped_mountain_above_lethal(self):
        return self._damage_scene('self_creature', 1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_tapped_mountain_below_lethal(self):
        return self._damage_scene('enemy_player', -1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_tapped_mountain_equal_lethal(self):
        return self._damage_scene('enemy_player', 0, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_tapped_mountain_above_lethal(self):
        return self._damage_scene('enemy_player', 1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_tapped_mountain_below_lethal(self):
        return self._damage_scene('self_player', -1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_tapped_mountain_equal_lethal(self):
        return self._damage_scene('self_player', 0, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_tapped_mountain_above_lethal(self):
        return self._damage_scene('self_player', 1, branch=0)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_untapped_mountain_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_untapped_mountain_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_untapped_mountain_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_untapped_mountain_below_lethal(self):
        return self._damage_scene('self_creature', -1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_untapped_mountain_equal_lethal(self):
        return self._damage_scene('self_creature', 0, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_creature_untapped_mountain_above_lethal(self):
        return self._damage_scene('self_creature', 1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_untapped_mountain_below_lethal(self):
        return self._damage_scene('enemy_player', -1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_untapped_mountain_equal_lethal(self):
        return self._damage_scene('enemy_player', 0, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_untapped_mountain_above_lethal(self):
        return self._damage_scene('enemy_player', 1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_untapped_mountain_below_lethal(self):
        return self._damage_scene('self_player', -1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_untapped_mountain_equal_lethal(self):
        return self._damage_scene('self_player', 0, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_self_player_untapped_mountain_above_lethal(self):
        return self._damage_scene('self_player', 1, branch=1)

    @simulate(evidence={'text': ('damage.base', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_hexproof_target(self):
        return self._damage_scene("enemy_creature", 1, branch=None, target_flags={"Hexproof": True})

