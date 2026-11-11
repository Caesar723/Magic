from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Temporal_Shift.model import Temporal_Shift


@bind_card(Temporal_Shift)
class Temporal_Shift_Simulation(Card_Simulation):
    scenario_locks={
        '_protection_scene':('opponent.battlefield', 'self.battlefield', 'self.library'),
    }

    text_parts = {
        "target.scope": [
            "Apply this to the selected creatures. Choose {freeze_count} opposing creatures randomly, or all if fewer are available.",
            "Affect the selected creatures. Choose {freeze_count} opposing creatures randomly, or all if fewer are available.",
            "Use the following effects on the selection. Choose {freeze_count} opposing creatures randomly, or all if fewer are available.",
            "The following effects apply to the chosen creatures. Choose {freeze_count} opposing creatures randomly, or all if fewer are available.",
            "Apply these effects to the chosen creatures. Choose {freeze_count} opposing creatures randomly, or all if fewer are available.",
            "Only the selected creatures receive these effects. Choose {freeze_count} opposing creatures randomly, or all if fewer are available.",
            "Affect the chosen set of creatures. Choose {freeze_count} opposing creatures randomly, or all if fewer are available.",
            "Apply this effect to the chosen set. Choose {freeze_count} opposing creatures randomly, or all if fewer are available.",
            "Use this on the selected opposing creatures. Choose {freeze_count} opposing creatures randomly, or all if fewer are available.",
            "Apply the effects below to the selected creatures. Choose {freeze_count} opposing creatures randomly, or all if fewer are available.",
        ],
        "freeze.effect": [
            "It counts as tapped until its controller's end step.",
            "Treat it as tapped until its controller's turn ends.",
            "Its tapped status is forced until the end of its controller's turn.",
            "Until its controller's end step, it is treated as tapped.",
            "The creature reports being tapped until its controller's turn ends.",
            "Keep its tapped status true until its controller's end step.",
            "It is considered tapped until the end step of its controller.",
            "Apply a tapped-status override until its controller's turn ends.",
            "Its tapped check returns true until its controller's end step.",
            "The creature is frozen as tapped until its controller's end step.",
        ],
        "stats.effect": [
            "Permanently reduce its remaining health by half, rounding the reduction up.",
            "Its remaining health becomes half, rounded down, as a permanent change.",
            "Reduce its health permanently by the ceiling of half its current remaining health.",
            "Leave it with half its current health, rounded down, with no turn expiry.",
            "Permanently subtract half its remaining health rounded upward.",
            "Apply a permanent health loss equal to half its remaining health rounded up.",
            "The creature permanently loses half its current health, rounding the loss up.",
            "Halve its remaining health and round the result downward, with a permanent adjustment.",
            "Its current remaining health is halved, rounding down, through a permanent debuff.",
            "Make a permanent health reduction of half its remaining health rounded up.",
        ],
        "time.effect": [
            "Add one time counter. If your time counter total reaches 10, reset it to zero and gain one extra turn.",
            "You gain a time counter. If your time counter total reaches 10, reset it to zero and gain one extra turn.",
            "Increase your time counters by one. If your time counter total reaches 10, reset it to zero and gain one extra turn.",
            "Put one time counter on yourself. If your time counter total reaches 10, reset it to zero and gain one extra turn.",
            "Gain one additional time counter. If your time counter total reaches 10, reset it to zero and gain one extra turn.",
            "Add a single time counter to your total. If your time counter total reaches 10, reset it to zero and gain one extra turn.",
            "Your time counter total increases by one. If your time counter total reaches 10, reset it to zero and gain one extra turn.",
            "Receive one time counter. If your time counter total reaches 10, reset it to zero and gain one extra turn.",
            "Increment your time counter count by one. If your time counter total reaches 10, reset it to zero and gain one extra turn.",
            "Place one more time counter on yourself. If your time counter total reaches 10, reset it to zero and gain one extra turn.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _protection_scene(self,own_count,enemy_count,health=3,tapped=False,knight=False,creature_knight=False,library_count=None,time_count=0):
        library_count=self.scenario_count("library",library_count)
        self.scenario_prepare()
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                creature = self.scenario_creature(owner, power=index + 1, health=health + index, flags={"tap": tapped, "Hexproof": owner is self.player.opponent and index % 2 == 0})
                if knight:
                    creature.type_card = "Human Knight"
                if creature_knight:
                    creature.type_creature = "Knight"
        if library_count is not None:
            self.scenario_replace_cards(self.player,"library",instant=(library_count, library_count))
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        self.player.counter_dict["time_counter"] = time_count
        return self.scenario_cast()

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_1(self):
        return self._protection_scene(0,0,health=1)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_2(self):
        return self._protection_scene(0,0,health=2)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_3(self):
        return self._protection_scene(0,0,health=3)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_5(self):
        return self._protection_scene(0,0,health=5)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_1(self):
        return self._protection_scene(1,0,health=1)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_2(self):
        return self._protection_scene(1,0,health=2)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_3(self):
        return self._protection_scene(1,0,health=3)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_5(self):
        return self._protection_scene(1,0,health=5)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_1(self):
        return self._protection_scene(0,1,health=1)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_2(self):
        return self._protection_scene(0,1,health=2)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_3(self):
        return self._protection_scene(0,1,health=3)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_5(self):
        return self._protection_scene(0,1,health=5)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_1(self):
        return self._protection_scene(1,1,health=1)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_2(self):
        return self._protection_scene(1,1,health=2)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_3(self):
        return self._protection_scene(1,1,health=3)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_5(self):
        return self._protection_scene(1,1,health=5)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_1(self):
        return self._protection_scene(3,3,health=1)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_2(self):
        return self._protection_scene(3,3,health=2)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_3(self):
        return self._protection_scene(3,3,health=3)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_5(self):
        return self._protection_scene(3,3,health=5)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_1(self):
        return self._protection_scene(0,5,health=1)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_2(self):
        return self._protection_scene(0,5,health=2)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_3(self):
        return self._protection_scene(0,5,health=3)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_5(self):
        return self._protection_scene(0,5,health=5)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_already_tapped(self):
        return self._protection_scene(3,3,tapped=True)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_time_0(self):
        return self._protection_scene(1,3,time_count=0)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_time_8(self):
        return self._protection_scene(1,3,time_count=8)

    @simulate(evidence={'text': ('target.scope', 'freeze.effect', 'stats.effect', 'time.effect'), 'fields': ('mana_cost',)})
    def simulate_time_9(self):
        return self._protection_scene(1,3,time_count=9)

