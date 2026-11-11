from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Cinder_Needle.model import Cinder_Needle


@bind_card(Cinder_Needle)
class Cinder_Needle_Simulation(Card_Simulation):
    text_parts = {
        "damage.base": [
            "{card_name} deals {damage} damage to a target opposing creature.",
            "Deal {damage} damage to a chosen opposing creature.",
            "Target opposing creature takes {damage} damage from {card_name}.",
            "{card_name} inflicts {damage} damage on a target opposing creature.",
            "Choose an opposing creature and deal {damage} damage to it.",
            "Hit a target opposing creature for {damage} damage.",
            "An opposing creature of your choice is dealt {damage} damage.",
            "{card_name} deals {damage} damage to the opposing creature you target.",
            "Deal a target opposing creature an amount of damage equal to {damage}.",
            "Target an opposing creature to be dealt {damage} damage by {card_name}.",
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

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_normal_below_lethal(self):
        return self._damage_scene('enemy_creature', -1, branch=None)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_normal_equal_lethal(self):
        return self._damage_scene('enemy_creature', 0, branch=None)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_normal_above_lethal(self):
        return self._damage_scene('enemy_creature', 1, branch=None)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_hexproof_target(self):
        return self._damage_scene("enemy_creature", 1, branch=None, target_flags={"Hexproof": True})

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_no_opponent_creatures(self):
        self.scenario_prepare()
        self.scenario_creature(self.player, flags={})
        return self.scenario_cast((1,))

