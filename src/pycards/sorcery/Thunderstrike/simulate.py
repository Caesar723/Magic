from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Thunderstrike.model import Thunderstrike


@bind_card(Thunderstrike)
class Thunderstrike_Simulation(Card_Simulation):
    text_parts = {
        "target.scope": [
            "Choose a target creature.",
            "Target one creature.",
            "Select a creature as the target.",
            "Choose one creature to target.",
            "Select a target creature.",
            "Choose any creature as your target.",
            "Target a creature of your choice.",
            "Choose a creature as the target for this spell.",
            "Select one creature to target.",
            "Choose a creature as your target.",
        ],
        "damage.effect": [
            "{card_name} deals {damage} damage to that creature.",
            "Deal {damage} damage to the chosen creature.",
            "That creature takes {damage} damage from {card_name}.",
            "{card_name} inflicts {damage} damage on that creature.",
            "The selected creature is dealt {damage} damage.",
            "Hit the target creature for {damage} damage.",
            "Inflict {damage} damage on the chosen target.",
            "{card_name} strikes that creature for {damage} damage.",
            "Deal that creature an amount of damage equal to {damage}.",
            "The targeted creature takes a total of {damage} damage.",
        ],
        "splash.condition": [
            "If that creature immediately dies with non-positive remaining health,",
            "If the target dies and its health is zero or less immediately after this damage,",
            "When the creature is dead with health at or below zero right after this hit,",
            "If it is immediately dead and its remaining health is not positive,",
            "If this hit leaves the creature dead with zero or negative health,",
            "When that creature immediately dies and has no positive health remaining,",
            "If the target is dead immediately after the hit and its health is non-positive,",
            "If that creature dies directly from the hit and is left with at most zero health,",
            "When the hit leaves that creature dead with health of zero or less,",
            "If the creature immediately ends up dead with non-positive health,",
        ],
        "splash.effect": [
            "add its remaining health to {damage} and deal that adjusted damage to every other opposing creature and to your opponent.",
            "calculate {damage} plus its remaining health, then deal that amount to all other opposing creatures and the opposing player.",
            "deal {damage} plus its post-hit health as damage to each other opposing creature and your opponent.",
            "adjust {damage} by adding its remaining health, then hit every other opposing creature and your opponent for that amount.",
            "use {damage} plus its non-positive remaining health as the damage dealt to all other opposing creatures and the opposing player.",
            "add the creature's post-hit health to {damage}, then deal the result to your opponent and each other opposing creature.",
            "calculate the adjusted damage as {damage} plus that remaining health and apply it to every other opposing creature and your opponent.",
            "deal an amount equal to {damage} plus the target's post-hit health to all other opposing creatures and the opposing player.",
            "add its remaining health to the original {damage} and deal the resulting damage to each other opposing creature and your opponent.",
            "combine {damage} with its remaining health and deal the total to your opponent and all other opposing creatures.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _damage_scene(self, target_role, life_offset, branch=None, target_flags=None, enemy_count=0):
        self.scenario_prepare()
        params = self.card.effect_params
        damage = params.get("damage", params.get("damage_low", 0))
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
        for index in range(enemy_count):
            self.scenario_creature(self.player.opponent, power=1, health=max(1, life + index - 1), flags={})
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast((subaction,), provide_mana=False)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_normal_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_normal_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_normal_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_normal_below_lethal(self):
        return self._damage_scene('self_creature', -1, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_normal_equal_lethal(self):
        return self._damage_scene('self_creature', 0, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_normal_above_lethal(self):
        return self._damage_scene('self_creature', 1, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_normal_below_lethal(self):
        return self._damage_scene('enemy_player', -1, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_normal_equal_lethal(self):
        return self._damage_scene('enemy_player', 0, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_player_normal_above_lethal(self):
        return self._damage_scene('enemy_player', 1, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_player_normal_below_lethal(self):
        return self._damage_scene('self_player', -1, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_player_normal_equal_lethal(self):
        return self._damage_scene('self_player', 0, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_self_player_normal_above_lethal(self):
        return self._damage_scene('self_player', 1, branch=None)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_hexproof_target(self):
        return self._damage_scene("enemy_creature", 1, branch=None, target_flags={"Hexproof": True})

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_self_creature_0_overkill(self):
        return self._damage_scene('self_creature', -1, enemy_count=0)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_self_creature_0_exact(self):
        return self._damage_scene('self_creature', 0, enemy_count=0)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_self_creature_0_survives(self):
        return self._damage_scene('self_creature', 1, enemy_count=0)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_self_creature_1_overkill(self):
        return self._damage_scene('self_creature', -1, enemy_count=1)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_self_creature_1_exact(self):
        return self._damage_scene('self_creature', 0, enemy_count=1)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_self_creature_1_survives(self):
        return self._damage_scene('self_creature', 1, enemy_count=1)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_self_creature_3_overkill(self):
        return self._damage_scene('self_creature', -1, enemy_count=3)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_self_creature_3_exact(self):
        return self._damage_scene('self_creature', 0, enemy_count=3)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_self_creature_3_survives(self):
        return self._damage_scene('self_creature', 1, enemy_count=3)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_low_remaining_health_self_creature(self):
        return self._damage_scene('self_creature', 1 - self.card.effect_params["damage"], enemy_count=3)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_enemy_creature_0_overkill(self):
        return self._damage_scene('enemy_creature', -1, enemy_count=0)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_enemy_creature_0_exact(self):
        return self._damage_scene('enemy_creature', 0, enemy_count=0)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_enemy_creature_0_survives(self):
        return self._damage_scene('enemy_creature', 1, enemy_count=0)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_enemy_creature_1_overkill(self):
        return self._damage_scene('enemy_creature', -1, enemy_count=1)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_enemy_creature_1_exact(self):
        return self._damage_scene('enemy_creature', 0, enemy_count=1)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_enemy_creature_1_survives(self):
        return self._damage_scene('enemy_creature', 1, enemy_count=1)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_enemy_creature_3_overkill(self):
        return self._damage_scene('enemy_creature', -1, enemy_count=3)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_enemy_creature_3_exact(self):
        return self._damage_scene('enemy_creature', 0, enemy_count=3)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_splash_enemy_creature_3_survives(self):
        return self._damage_scene('enemy_creature', 1, enemy_count=3)

    @simulate(evidence={'text': ('target.scope', 'damage.effect', 'splash.condition', 'splash.effect'), 'fields': ('mana_cost',)})
    def simulate_low_remaining_health_enemy_creature(self):
        return self._damage_scene('enemy_creature', 1 - self.card.effect_params["damage"], enemy_count=3)

