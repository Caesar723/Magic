from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.Instant.Timeless_Intervention.model import Timeless_Intervention


@bind_card(Timeless_Intervention)
class Timeless_Intervention_Simulation(Card_Simulation):
    scenario_locks={
        '_board_scene':('opponent.battlefield', 'opponent.exile_area', 'opponent.land_area', 'self.battlefield', 'self.exile_area', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "exile.effect": [
            "Exile all creatures.",
            "Exile every creature on both battlefields.",
            "Remove all creatures from play into exile.",
            "Put every creature in play into exile.",
            "Exile each creature on either battlefield.",
            "All creatures on both sides are exiled.",
            "Every creature in play goes into exile.",
            "Move the creatures on both battlefields into exile.",
            "Exile all creatures controlled by either player.",
            "Send every creature on the battlefield into exile.",
        ],
        "return.delayed": [
            "At the beginning of your next turn, return all creatures in either player's exile area to their owners' battlefields.",
            "When your next turn begins, return every exiled creature to its owner's battlefield.",
            "At your next turn start, put all creatures from both exile areas back onto their owners' battlefields.",
            "When you next begin a turn, return all exiled creatures under their owners' control.",
            "At the start of your next turn, bring back every creature in either exile area for its owner.",
            "On your next turn's beginning, all creatures in both exile areas return to their owners' battlefields.",
            "Return every creature in either player's exile area to its owner when your next turn starts.",
            "Your next turn begins by returning all exiled creatures to their owners' battlefields.",
            "At your next turn start, each owner gets back all creatures in their exile area.",
            "When your following turn starts, restore all creatures from both exile areas to their owners' battlefields.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _board_scene(self,own_count,enemy_count,protected=False,library_count=None,life=None,old_exile=False):
        library_count=self.scenario_count("library",library_count)
        self.scenario_prepare()
        if life is not None:
            if not 1 <= life <= self.player.ini_life:
                return self.scenario_skip()
            self.player.life = life
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                creature = self.scenario_creature(owner, power=2 + index, health=3 + index, flags={"Hexproof": index % 2 == 0, "tap": index % 2 == 1})
                if protected:
                    self.scenario_buff(creature, Indestructible(self.card, creature))
            land = Plains(owner)
            self.scenario_tapped(land)
            self.stage_card(land, owner, zone="land_area")
            if old_exile:
                creature = self.scenario_creature(owner, power=1, health=2, flags={}, zone="exile_area")
        if library_count is not None:
            self.scenario_replace_cards(self.player,"library",instant=(library_count, library_count))
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('exile.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_normal(self):
        return self._board_scene(0,0)

    @simulate(evidence={'text': ('exile.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_normal(self):
        return self._board_scene(1,0)

    @simulate(evidence={'text': ('exile.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_normal(self):
        return self._board_scene(0,1)

    @simulate(evidence={'text': ('exile.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_normal(self):
        return self._board_scene(1,1)

    @simulate(evidence={'text': ('exile.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_normal(self):
        return self._board_scene(3,3)

    @simulate(evidence={'text': ('exile.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_normal(self):
        return self._board_scene(0,5)

    @simulate(evidence={'text': ('exile.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_normal(self):
        return self._board_scene(5,0)

    @simulate(evidence={'text': ('exile.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_protected_battlefields(self):
        return self._board_scene(3,3,protected=True)

    @simulate(evidence={'text': ('exile.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_old_exiled_creatures(self):
        return self._board_scene(2,2,old_exile=True)

