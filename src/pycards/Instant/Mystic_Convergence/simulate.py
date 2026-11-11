from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Mystic_Convergence.model import Mystic_Convergence


@bind_card(Mystic_Convergence)
class Mystic_Convergence_Simulation(Card_Simulation):
    text_parts = {
        "combat.effect": [
            "Until your next upkeep, whenever anything is damaged while combat is active, heal that object for the damage amount.",
            "While combat is active before your next upkeep, restore the amount of damage dealt to each damaged creature or player.",
            "Whenever a creature or player takes damage during an active combat before your next upkeep, heal it by that amount.",
            "Before your next upkeep, heal each object by the damage it receives whenever the room is in combat.",
            "Until your next turn begins, damage received during an active combat is followed by healing for the same amount.",
            "When combat is active before your next upkeep, give the damaged creature or player healing equal to the damage.",
            "Until your next upkeep, each active-combat damage event triggers equal healing for its recipient.",
            "Heal damage recipients by the amount they take during active combat until your next upkeep.",
            "Before your next turn starts, restore damage recipients by their damage amount while combat is active.",
            "Until your next upkeep, whenever combat is active and damage is received, heal its recipient by that amount.",
        ],
        "mana.effect": [
            "At your next upkeep, add mana equal to the total healing-trigger damage, split evenly among five colors with the remainder in R.",
            "When your next turn begins, turn the accumulated damage into mana, giving each color an equal integer share and R the remainder.",
            "At your next upkeep, generate the recorded damage amount as mana, dividing evenly over five colors and putting leftover mana into R.",
            "On your next turn start, add the accumulated damage total as five-color mana with equal integer shares and any remainder assigned to R.",
            "At your next upkeep, the recorded damage becomes mana equally shared among U, B, R, G, W, with all remainder in R.",
            "When your following turn starts, add the damage total in mana, sharing equally across five colors and adding the remainder to R.",
            "Convert the accumulated damage into mana at your next upkeep, giving each color the quotient by five and R the remainder.",
            "At the beginning of your next turn, generate mana matching the collected damage, evenly divided with extra remainder in R.",
            "Your next upkeep adds mana for all collected damage, divided into equal five-color shares with the leftover in R.",
            "At your next turn start, gain mana equal to collected damage, distributing equal integer shares to each color and the remainder to R.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _combat_scene(self, own_count, enemy_count, missing=1, attacker=False):
        self.scenario_prepare()
        self.player.life = max(1, self.player.ini_life - missing)
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                self.scenario_creature(owner, power=index + 1, health=index + 3, flags={})
        if attacker:
            creature = self.scenario_creature(self.player.opponent, power=2, health=4, flags={})
            creature.set_counter_dict("attack_counter", 1)
            self.room.attacker = creature
        record = self.scenario_cast(in_stack=attacker)
        if attacker:
            self.room.flag_dict["attacker_defenders"] = True
            self.room.non_active_player = self.player
        return record

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_attacking_False(self):
        return self._combat_scene(0, 0, attacker=False)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_attacking_True(self):
        return self._combat_scene(0, 0, attacker=True)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_attacking_False(self):
        return self._combat_scene(1, 0, attacker=False)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_attacking_True(self):
        return self._combat_scene(1, 0, attacker=True)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_attacking_False(self):
        return self._combat_scene(0, 1, attacker=False)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_attacking_True(self):
        return self._combat_scene(0, 1, attacker=True)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_attacking_False(self):
        return self._combat_scene(1, 1, attacker=False)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_attacking_True(self):
        return self._combat_scene(1, 1, attacker=True)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_attacking_False(self):
        return self._combat_scene(3, 3, attacker=False)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_attacking_True(self):
        return self._combat_scene(3, 3, attacker=True)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_life_full(self):
        return self._combat_scene(2, 2, missing=0)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_life_near_full(self):
        return self._combat_scene(2, 2, missing=1)

    @simulate(evidence={'text': ('combat.effect', 'mana.effect'), 'fields': ('mana_cost',)})
    def simulate_life_injured(self):
        return self._combat_scene(2, 2, missing=self.player.ini_life - 1)

