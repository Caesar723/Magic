from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.sorcery.Soul_Siphon.model import Soul_Siphon


@bind_card(Soul_Siphon)
class Soul_Siphon_Simulation(Card_Simulation):
    text_parts = {
        "target.selection": [
            "If your opponent controls any creatures, choose one at random.",
            "If an opposing creature is present, randomly select one of them.",
            "Choose a random creature your opponent controls, if any.",
            "When your opponent has a creature, select one of their creatures randomly.",
            "If the opposing battlefield has any creatures, pick one at random.",
            "Randomly select an opposing creature if one is available.",
            "If your opponent has creatures in play, choose one randomly.",
            "Pick a creature at random from your opponent's battlefield when it is nonempty.",
            "When an opposing creature is available, choose one at random.",
            "If any creatures are under your opponent's control, select one randomly.",
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
        "heal.effect": [
            "You gain life equal to that creature's power.",
            "Gain an amount of life equal to the selected creature's power.",
            "You restore life equal to that creature's power.",
            "Increase your life total by the power of that creature.",
            "Gain life matching the power of the creature you chose.",
            "You gain an amount of life matching that creature's power.",
            "Restore to yourself an amount of life equal to that creature's power.",
            "Gain as much life as the power of that selected creature.",
            "The selected creature's power determines how much life you gain.",
            "You gain life matching the selected creature's power.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _random_scene(self, own_count, enemy_count, missing=1, damaged=False):
        self.scenario_prepare()
        self.player.life = max(1, self.player.ini_life - missing)
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                creature = self.scenario_creature(owner, power=index + 1, health=index + 2, flags={})
                if damaged:
                    creature.live += 5
        return self.scenario_cast()

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_full(self):
        return self._random_scene(0, 0, 0)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_near_full(self):
        return self._random_scene(0, 0, 1)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_injured(self):
        return self._random_scene(0, 0, self.player.ini_life - 1)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_full(self):
        return self._random_scene(1, 0, 0)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_near_full(self):
        return self._random_scene(1, 0, 1)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_injured(self):
        return self._random_scene(1, 0, self.player.ini_life - 1)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_full(self):
        return self._random_scene(0, 1, 0)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_near_full(self):
        return self._random_scene(0, 1, 1)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_injured(self):
        return self._random_scene(0, 1, self.player.ini_life - 1)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_full(self):
        return self._random_scene(1, 1, 0)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_near_full(self):
        return self._random_scene(1, 1, 1)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_injured(self):
        return self._random_scene(1, 1, self.player.ini_life - 1)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_full(self):
        return self._random_scene(3, 3, 0)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_near_full(self):
        return self._random_scene(3, 3, 1)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_injured(self):
        return self._random_scene(3, 3, self.player.ini_life - 1)

    @simulate(evidence={'text': ('target.selection', 'remove.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_damaged_creatures(self):
        return self._random_scene(1, 1, self.player.ini_life - 1, True)

