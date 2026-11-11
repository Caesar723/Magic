from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Fiery_Burst.model import Fiery_Burst


@bind_card(Fiery_Burst)
class Fiery_Burst_Simulation(Card_Simulation):
    scenario_locks={
        '_damage_scene':('self.land_area',),
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
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _damage_scene(self,target_role,life_offset,target_flags=None):
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
        return self._damage_scene('enemy_creature',-1)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_normal_equal_lethal(self):
        return self._damage_scene('enemy_creature',0)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_normal_above_lethal(self):
        return self._damage_scene('enemy_creature',1)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_self_creature_normal_below_lethal(self):
        return self._damage_scene('self_creature',-1)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_self_creature_normal_equal_lethal(self):
        return self._damage_scene('self_creature',0)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_self_creature_normal_above_lethal(self):
        return self._damage_scene('self_creature',1)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_enemy_player_normal_below_lethal(self):
        return self._damage_scene('enemy_player',-1)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_enemy_player_normal_equal_lethal(self):
        return self._damage_scene('enemy_player',0)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_enemy_player_normal_above_lethal(self):
        return self._damage_scene('enemy_player',1)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_self_player_normal_below_lethal(self):
        return self._damage_scene('self_player',-1)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_self_player_normal_equal_lethal(self):
        return self._damage_scene('self_player',0)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_self_player_normal_above_lethal(self):
        return self._damage_scene('self_player',1)

    @simulate(evidence={'text': ('damage.base',), 'fields': ('mana_cost',)})
    def simulate_hexproof_target(self):
        return self._damage_scene("enemy_creature",1,target_flags={"Hexproof": True})

