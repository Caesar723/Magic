from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.sorcery.Divine_Intervention.model import Divine_Intervention


@bind_card(Divine_Intervention)
class Divine_Intervention_Simulation(Card_Simulation):
    scenario_locks={
        '_board_scene':('opponent.battlefield', 'opponent.land_area', 'self.battlefield', 'self.land_area', 'self.library'),
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
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _board_scene(self,own_count,enemy_count,protected=False,library_count=None,life=None):
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
        if library_count is not None:
            self.scenario_replace_cards(self.player,"library",instant=(library_count, library_count))
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('exile.effect',), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_normal(self):
        return self._board_scene(0,0)

    @simulate(evidence={'text': ('exile.effect',), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_normal(self):
        return self._board_scene(1,0)

    @simulate(evidence={'text': ('exile.effect',), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_normal(self):
        return self._board_scene(0,1)

    @simulate(evidence={'text': ('exile.effect',), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_normal(self):
        return self._board_scene(1,1)

    @simulate(evidence={'text': ('exile.effect',), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_normal(self):
        return self._board_scene(3,3)

    @simulate(evidence={'text': ('exile.effect',), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_normal(self):
        return self._board_scene(0,5)

    @simulate(evidence={'text': ('exile.effect',), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_normal(self):
        return self._board_scene(5,0)

    @simulate(evidence={'text': ('exile.effect',), 'fields': ('mana_cost',)})
    def simulate_protected_battlefields(self):
        return self._board_scene(3,3,protected=True)

