from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Mystic_Reflection.model import Mystic_Reflection


@bind_card(Mystic_Reflection)
class Mystic_Reflection_Simulation(Card_Simulation):
    scenario_locks={
        '_target_scene':('opponent.battlefield', 'self.battlefield'),
        'simulate_without_mana':('self.battlefield',),
        'simulate_no_creatures':('opponent.battlefield', 'self.battlefield'),
        'simulate_wounded_largest':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts={
        "clone.effect": [
            "Target creature becomes a copy of a creature on either battlefield with the greatest combined current power and toughness until the end of its controller's turn. If tied, choose one at random.",
            "Until its controller's turn ends, target creature copies a creature from either battlefield whose current power plus toughness is greatest. Choose randomly among tied creatures.",
            "Choose a target creature. It copies a creature with the highest current power-and-toughness total across both battlefields until its controller's turn ends, with ties chosen at random.",
            "Target a creature and make it a copy of a creature with the largest sum of current power and toughness on either battlefield until its controller's turn ends. Select randomly if tied.",
            "Target creature temporarily copies a creature with the greatest current power plus toughness among both players' battlefield creatures. This lasts until its controller's turn ends, and ties are random.",
            "Find the greatest current power-and-toughness sum among creatures on either battlefield. Target creature copies a randomly chosen creature with that sum until the end of its controller's turn.",
            "Until the end of its controller's turn, target creature becomes a copy of one of the battlefield creatures with the highest current power plus toughness, chosen randomly in a tie.",
            "From both battlefields, randomly choose a creature tied for the greatest combined current power and toughness. Target creature becomes its copy until its controller's turn ends.",
            "Make target creature copy a creature whose current power and toughness add up to the largest total on either battlefield, choosing randomly among ties. The copy lasts until its controller's turn ends.",
            "Target creature copies a creature from either player's battlefield with the greatest sum of current power and toughness until the end of its controller's turn. Break any tie at random.",
        ]
    }

    def _target_scene(self,own_target=True,reference_enemy=False,target_stats=(2,4),reference_stats=(6,6),tie=False,hexproof=False):
        self.scenario_prepare()
        owner=self.player if own_target else self.player.opponent
        target=self.scenario_creature(owner,*target_stats,flags={"Hexproof":hexproof})
        target.name="Chosen creature"
        if reference_stats is not None:
            owner=self.player.opponent if reference_enemy else self.player
            reference=self.scenario_creature(owner,*reference_stats,flags={"reach":True})
            reference.name="Largest creature"
            if tie:
                other=self.scenario_creature(owner.opponent,reference_stats[0]+1,reference_stats[1]-1,flags={"flying":True})
                other.name="Tied largest creature"
        return self.scenario_cast((11 if own_target else 1,))

    @simulate(evidence={"fields":("mana_cost",)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_creature(self.player,power=2,health=4,flags={})
        return self.scenario_cast((11,),provide_mana=False)

    @simulate(evidence={"fields":("mana_cost",)})
    def simulate_no_creatures(self):
        self.scenario_prepare()
        return self.scenario_cast((1,11))

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_only_own_creature(self):
        return self._target_scene(reference_stats=None)

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_only_enemy_creature(self):
        return self._target_scene(False,reference_stats=None)

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_own_target_own_largest(self):
        return self._target_scene()

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_own_target_enemy_largest(self):
        return self._target_scene(reference_enemy=True)

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_enemy_target_own_largest(self):
        return self._target_scene(False)

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_enemy_target_enemy_largest(self):
        return self._target_scene(False,True)

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_own_target_already_largest(self):
        return self._target_scene(target_stats=(9,9))

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_enemy_target_already_largest(self):
        return self._target_scene(False,target_stats=(9,9))

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_tied_largest(self):
        return self._target_scene(tie=True)

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_target_tied_for_largest(self):
        return self._target_scene(reference_stats=(3,3))

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_same_power_more_health(self):
        return self._target_scene(reference_stats=(2,5))

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_same_health_more_power(self):
        return self._target_scene(reference_stats=(3,4))

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_more_power_smaller_total(self):
        return self._target_scene(target_stats=(10,1),reference_stats=(5,8))

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_more_health_larger_total(self):
        return self._target_scene(target_stats=(0,15),reference_stats=(10,4))

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_negative_power(self):
        return self._target_scene(target_stats=(-2,3),reference_stats=(0,2))

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_own_hexproof_target(self):
        return self._target_scene(hexproof=True)

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_enemy_hexproof_target(self):
        return self._target_scene(False,hexproof=True)

    @simulate(evidence={"text":("clone.effect",),"fields":("mana_cost",)})
    def simulate_wounded_largest(self):
        self.scenario_prepare()
        self.scenario_creature(self.player,power=2,health=4,flags={})
        wounded=self.scenario_creature(self.player.opponent,power=10,health=10,flags={})
        wounded.actual_live=1
        self.scenario_creature(self.player.opponent,power=6,health=6,flags={"reach":True})
        return self.scenario_cast((11,))
