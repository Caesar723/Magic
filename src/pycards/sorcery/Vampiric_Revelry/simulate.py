from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.sorcery.Vampiric_Revelry.model import Vampiric_Revelry


@bind_card(Vampiric_Revelry)
class Vampiric_Revelry_Simulation(Card_Simulation):
    scenario_locks={
        '_random_scene':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
        "target.selection": [
            "If either player controls a creature, choose one at random.",
            "If a creature is present, randomly select one of them.",
            "Choose a random creature on either battlefield, if any.",
            "When either player has a creature, select one creature from both battlefields randomly.",
            "If either battlefield has any creatures, pick one at random.",
            "Randomly select a creature if one is available.",
            "If either player has creatures in play, choose one randomly.",
            "Pick a creature at random from both battlefields when it is nonempty.",
            "When a creature is available, choose one at random.",
            "If any creatures are on either battlefield, select one randomly.",
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
            "You gain life equal to that creature's remaining health, with a minimum of zero.",
            "Gain as much life as that creature's current health, treating negative health as zero.",
            "You restore life equal to its remaining health, counting any negative value as zero.",
            "Increase your life total by the chosen creature's remaining health, with a minimum gain of zero.",
            "Gain life matching the selected creature's current health, or zero if that health is negative.",
            "You gain life equal to the non-negative part of that creature's remaining health.",
            "Restore to yourself the selected creature's current health in life, with a minimum of zero.",
            "Gain life equal to its remaining health, clamping negative health to zero.",
            "Use that creature's current remaining health as your life gain, with negative values replaced by zero.",
            "You gain an amount of life equal to its remaining health or zero, whichever is greater.",
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

