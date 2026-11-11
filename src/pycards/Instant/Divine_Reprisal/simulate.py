from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.Instant.Divine_Reprisal.model import Divine_Reprisal


@bind_card(Divine_Reprisal)
class Divine_Reprisal_Simulation(Card_Simulation):
    scenario_locks={
        '_target_scene':('opponent.battlefield', 'self.battlefield'),
        'simulate_no_creatures':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
        "target.scope": [
            "Choose a target opposing creature.",
            "Target one opposing creature.",
            "Select a opposing creature as the target.",
            "Choose one opposing creature to target.",
            "Select a target opposing creature.",
            "Choose any opposing creature as your target.",
            "Target a opposing creature of your choice.",
            "Choose a opposing creature as the target for this spell.",
            "Select one opposing creature to target.",
            "Choose a opposing creature as your target.",
        ],
        "destroy.condition": [
            "If that creature is the current attacker,",
            "If the selected creature is currently attacking,",
            "When the target is the room's current attacking creature,",
            "If the chosen creature is the current attacker,",
            "If the selected target is the creature currently attacking,",
            "When the chosen target is the current attacker,",
            "If the target matches the current attacker,",
            "If that creature is the one currently attacking,",
            "When the target is currently the attacking creature,",
            "If your chosen creature is the current attacking creature,",
        ],
        "remove.effect": [
            "Destroy that creature.",
            "Destroy the targeted creature.",
            "Destroy the creature you chose.",
            "That creature is destroyed.",
            "The selected creature is destroyed.",
            "Destroy your chosen creature.",
            "Cause that creature to be destroyed.",
            "Destroy the chosen target.",
            "Have the targeted creature destroyed.",
            "Destroy the creature selected this way.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _target_scene(self, opponent, flags=None, power=3, current_power=None, health=5, missing=1, protected=False, attacking=False, other_attacker=False):
        self.scenario_prepare()
        owner = self.player.opponent if opponent else self.player
        target = self.scenario_creature(owner, power=power, health=health, flags=flags or {})
        if current_power is not None:
            target.actual_power = current_power
        if protected:
            self.scenario_buff(target, Indestructible(self.card, target))
        self.player.life = max(1, self.player.ini_life - missing)
        combat = attacking or other_attacker
        if combat:
            attacker = self.scenario_creature(self.player.opponent, power=1, health=3, flags={}) if other_attacker else target
            attacker.set_counter_dict("attack_counter", 1)
            self.room.attacker = attacker
            self.room.flag_dict["attacker_defenders"] = True
        subaction = 1 if opponent else 11
        record = self.scenario_cast((subaction,), in_stack=combat)
        if combat:
            self.room.active_player, self.room.non_active_player = self.player.opponent, self.player
            self.room.flag_dict["attacker_defenders"] = True
        return record

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_ready(self):
        return self._target_scene(False, {})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tapped(self):
        return self._target_scene(False, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_flying(self):
        return self._target_scene(False, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._target_scene(False, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_indestructible(self):
        return self._target_scene(False, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_attacking(self):
        return self._target_scene(False, attacking=True)

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_self_different_attacker(self):
        return self._target_scene(False, other_attacker=True)

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_ready(self):
        return self._target_scene(True, {})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tapped(self):
        return self._target_scene(True, {'tap': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_flying(self):
        return self._target_scene(True, {'flying': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(True, {'Hexproof': True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_indestructible(self):
        return self._target_scene(True, protected=True, flags={"flying": True, "tap": True})

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_attacking(self):
        return self._target_scene(True, attacking=True)

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_different_attacker(self):
        return self._target_scene(True, other_attacker=True)

    @simulate(evidence={'text': ('target.scope', 'destroy.condition', 'remove.effect'), 'fields': ('mana_cost',)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast()

