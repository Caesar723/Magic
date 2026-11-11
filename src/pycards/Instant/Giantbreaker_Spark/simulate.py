from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Giantbreaker_Spark.model import Giantbreaker_Spark


@bind_card(Giantbreaker_Spark)
class Giantbreaker_Spark_Simulation(Card_Simulation):
    scenario_locks={
        '_damage_scene':('self.land_area',),
        'simulate_no_opponent_creatures':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
        "damage.target": [
            "Choose a target creature your opponent controls.",
            "Target a creature your opponent controls.",
            "Choose any opposing creature your opponent controls as the target.",
            "Select a creature your opponent controls to target.",
            "Target any one creature your opponent controls.",
            "Choose one creature your opponent controls as a target.",
            "Select a target from among opposing creatures.",
            "Choose a creature your opponent controls to receive the damage.",
            "Select any opposing creature your opponent controls as your target.",
            "Choose the target from any opposing creature your opponent controls.",
        ],
        "damage.condition": [
            "If the target has power at least {power_threshold},",
            "If the target has power {power_threshold} or greater,",
            "When the target has power no lower than {power_threshold},",
            "If the target has at least {power_threshold} power,",
            "If the target's power is {power_threshold} or more,",
            "When the target has power at least {power_threshold},",
            "If the target has {power_threshold} or more power,",
            "If the target has power of at least {power_threshold},",
            "If the target's power is {power_threshold} or higher,",
            "When the target has power equal to or above {power_threshold},",
        ],
        "damage.high": [
            "{card_name} deals {damage_high} damage to that target.",
            "deal {damage_high} damage to the target.",
            "inflict {damage_high} damage on that creature.",
            "that creature takes {damage_high} damage.",
            "the target is dealt {damage_high} damage.",
            "{card_name} inflicts {damage_high} damage on the target.",
            "hit the targeted creature for {damage_high} damage.",
            "the targeted creature takes {damage_high} damage from {card_name}.",
            "deal an amount of damage equal to {damage_high} to that creature.",
            "{card_name} hits the target for {damage_high} damage.",
        ],
        "damage.low": [
            "Otherwise, {card_name} deals {damage_low} damage to that target.",
            "Otherwise, deal {damage_low} damage to the target.",
            "Otherwise, inflict {damage_low} damage on that creature.",
            "Otherwise, that creature takes {damage_low} damage.",
            "Otherwise, the target is dealt {damage_low} damage.",
            "Otherwise, {card_name} inflicts {damage_low} damage on the target.",
            "Otherwise, hit the targeted creature for {damage_low} damage.",
            "Otherwise, the targeted creature takes {damage_low} damage from {card_name}.",
            "Otherwise, deal an amount of damage equal to {damage_low} to that creature.",
            "Otherwise, {card_name} hits the target for {damage_low} damage.",
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
        power = max(0, params["power_threshold"] + branch)
        damage = params["damage_high"] if power >= params["power_threshold"] else params["damage_low"]
        life = damage + life_offset
        if life <= 0:
            return self.scenario_skip()
        if target_role in ("self_creature", "enemy_creature"):
            owner = self.player if target_role == "self_creature" else self.player.opponent
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

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.low'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_below_condition_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=-1)

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.low'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_below_condition_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=-1)

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.low'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_below_condition_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=-1)

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_equal_condition_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=0)

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_equal_condition_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=0)

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_equal_condition_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=0)

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_above_condition_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=1)

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_above_condition_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=1)

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.high'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_above_condition_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=1)

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.high', 'damage.low'), 'fields': ('mana_cost',)})
    def simulate_hexproof_target(self):
        return self._damage_scene("enemy_creature", 1, branch=0, target_flags={"Hexproof": True})

    @simulate(evidence={'text': ('damage.target', 'damage.condition', 'damage.high', 'damage.low'), 'fields': ('mana_cost',)})
    def simulate_no_opponent_creatures(self):
        self.scenario_prepare()
        self.scenario_creature(self.player, flags={})
        return self.scenario_cast((1,))

