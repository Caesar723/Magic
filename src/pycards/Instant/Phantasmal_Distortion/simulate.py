from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Phantasmal_Distortion.model import Phantasmal_Distortion


@bind_card(Phantasmal_Distortion)
class Phantasmal_Distortion_Simulation(Card_Simulation):
    scenario_locks={
        '_target_scene':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
        "clone.effect": [
            "Until your end step, a target creature you control copies the stats and methods of another random creature you control.",
            "Choose one of your creatures to copy another random friendly creature's stats and methods until your turn ends.",
            "Make a target creature you control copy a randomly chosen other friendly creature through your turn.",
            "Your target creature copies the stats and methods of one random other creature you control until your end step.",
            "Until your turn ends, let a chosen friendly creature copy another random creature under your control.",
            "A target friendly creature becomes a temporary copy of a random other friendly creature until your end step.",
            "Copy another randomly chosen friendly creature onto the targeted creature you control until your turn ends.",
            "Give one of your creatures the stats and methods of a random other friendly creature until your end step.",
            "The selected creature you control copies one random other creature on your battlefield through your turn.",
            "Until your end step, transform a target friendly creature by copying another random friendly creature's stats and methods.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _target_scene(self,own_target=True,others=1,same_name=True,counterpart_enemy=False,hexproof=False):
        self.scenario_prepare()
        owner = self.player if own_target else self.player.opponent
        target = self.scenario_creature(owner, power=2, health=4, flags={"Hexproof": hexproof})
        for index in range(others):
            other_owner = self.player.opponent if counterpart_enemy else self.player
            creature = self.scenario_creature(other_owner, power=3 + index, health=6 + index, flags={"reach": True})
            if same_name:
                creature.name = target.name
        subaction = 11 if own_target else 1
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('clone.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_False_others_0_same_True(self):
        return self._target_scene(False,0,same_name=True)

    @simulate(evidence={'text': ('clone.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_False_others_1_same_True(self):
        return self._target_scene(False,1,same_name=True)

    @simulate(evidence={'text': ('clone.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_False_others_3_same_True(self):
        return self._target_scene(False,3,same_name=True)

    @simulate(evidence={'text': ('clone.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_True_others_0_same_True(self):
        return self._target_scene(True,0,same_name=True)

    @simulate(evidence={'text': ('clone.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_True_others_1_same_True(self):
        return self._target_scene(True,1,same_name=True)

    @simulate(evidence={'text': ('clone.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_True_others_3_same_True(self):
        return self._target_scene(True,3,same_name=True)

    @simulate(evidence={'text': ('clone.effect',), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(False,hexproof=True)

