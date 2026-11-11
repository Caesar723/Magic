from pycards.creature.Eternal_Phoenix.model import Eternal_Phoenix
from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Soul_Transfer.model import Soul_Transfer


@bind_card(Soul_Transfer)
class Soul_Transfer_Simulation(Card_Simulation):
    text_parts = {
        "death.effect": [
            "Give a target creature the death methods of creature cards currently in your graveyard, in addition to its existing death method.",
            "A target creature gains the current graveyard creatures' death methods alongside its own.",
            "Add the death methods of creatures now in your graveyard to a target creature's existing death method.",
            "Grant the targeted creature the death methods found on your current graveyard creatures.",
            "The chosen creature receives death methods from creature cards presently in your graveyard in addition to its own.",
            "Append your current graveyard creatures' death methods to those of a target creature.",
            "Let the target creature also execute the death methods of creatures currently in your graveyard.",
            "A creature you target gains all non-default death methods on creature cards currently in your graveyard.",
            "Copy the current graveyard creatures' death methods onto a target creature while keeping its existing one.",
            "The target gains additional death methods from creature cards now in your graveyard.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _target_scene(self, own_target=True, others=1, same_name=True, counterpart_enemy=False, hexproof=False, donors=0):
        self.scenario_prepare()
        owner = self.player if own_target else self.player.opponent
        target = self.scenario_creature(owner, power=2, health=4, flags={"Hexproof": hexproof})
        for index in range(others):
            other_owner = self.player.opponent if counterpart_enemy else self.player
            creature = self.scenario_creature(other_owner, power=3 + index, health=6 + index, flags={"reach": True})
            if same_name:
                creature.name = target.name
        self.player.graveyard.clear()
        for _ in range(donors):
            self.player.append_card(Eternal_Phoenix(self.player), "graveyard")
        subaction = 11 if own_target else 1
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_False_others_0_same_True(self):
        return self._target_scene(False, 0, same_name=True)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_False_others_1_same_True(self):
        return self._target_scene(False, 1, same_name=True)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_False_others_3_same_True(self):
        return self._target_scene(False, 3, same_name=True)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_True_others_0_same_True(self):
        return self._target_scene(True, 0, same_name=True)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_True_others_1_same_True(self):
        return self._target_scene(True, 1, same_name=True)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_target_own_True_others_3_same_True(self):
        return self._target_scene(True, 3, same_name=True)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._target_scene(False, hexproof=True)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_death_own_False_donors_0(self):
        return self._target_scene(False, donors=0)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_death_own_False_donors_1(self):
        return self._target_scene(False, donors=1)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_death_own_False_donors_2(self):
        return self._target_scene(False, donors=2)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_death_own_True_donors_0(self):
        return self._target_scene(True, donors=0)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_death_own_True_donors_1(self):
        return self._target_scene(True, donors=1)

    @simulate(evidence={'text': ('death.effect',), 'fields': ('mana_cost',)})
    def simulate_death_own_True_donors_2(self):
        return self._target_scene(True, donors=2)

