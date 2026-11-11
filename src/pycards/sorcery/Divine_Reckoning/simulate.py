from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.sorcery.Divine_Reckoning.model import Divine_Reckoning


@bind_card(Divine_Reckoning)
class Divine_Reckoning_Simulation(Card_Simulation):
    scenario_locks={
        '_board_scene':('opponent.battlefield', 'opponent.land_area', 'self.battlefield', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "destroy.effect": [
            "Destroy every creature whose creature subtype does not contain Angel.",
            "Destroy all creatures without Angel in their creature subtype.",
            "Every creature that lacks Angel in its creature subtype is destroyed.",
            "Destroy each creature unless its creature subtype contains Angel.",
            "All creatures with no Angel in their creature subtype are destroyed.",
            "Destroy creatures on both battlefields whose creature subtype lacks Angel.",
            "Destroy all creatures other than those with Angel in their creature subtype.",
            "Each creature without Angel in its creature subtype is marked for destruction.",
            "Destroy the creatures on either side whose creature subtype does not include Angel.",
            "Destroy every creature except those whose creature subtype includes Angel.",
        ],
        "heal.effect": [
            "Each player gains one life for each of their creatures marked this way, even if protected from destruction.",
            "For every creature selected for destruction this way, its controller gains one life, including protected creatures.",
            "Count the attempted destructions for each player and give that player that much life, including attempts on protected creatures.",
            "Each player gains life equal to their creatures selected for destruction, even when protection keeps them alive.",
            "Give each player one life per creature of theirs this effect tried to destroy, including protected creatures.",
            "A player gains one life for each of their creatures targeted by this destruction, whether destruction succeeds or is prevented.",
            "Each controller restores one life per attempted destruction of their creatures, counting protected ones too.",
            "Gain for each player one life per creature selected for destruction on their side, even if it survives protection.",
            "Each player restores life equal to the number of their creatures this effect marked for destruction, including protected targets.",
            "Every attempted destruction grants the creature's controller one life, even if that creature cannot be destroyed.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _board_scene(self,own_count,enemy_count,offset=0,protected=False,library_count=None,life=None):
        library_count=self.scenario_count("library",library_count)
        self.scenario_prepare()
        if life is not None:
            if not 1 <= life <= self.player.ini_life:
                return self.scenario_skip()
            self.player.life = life
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                creature = self.scenario_creature(owner, power=2 + index, health=3 + index, flags={"Hexproof": index % 2 == 0, "tap": index % 2 == 1})
                creature.type_creature = "Angel" if (index + offset) % 2 == 0 else "Human"
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

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_below(self):
        return self._board_scene(0,0,offset=-1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_equal(self):
        return self._board_scene(0,0,offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_above(self):
        return self._board_scene(0,0,offset=1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_below(self):
        return self._board_scene(1,0,offset=-1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_equal(self):
        return self._board_scene(1,0,offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_above(self):
        return self._board_scene(1,0,offset=1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_below(self):
        return self._board_scene(0,1,offset=-1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_equal(self):
        return self._board_scene(0,1,offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_above(self):
        return self._board_scene(0,1,offset=1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_below(self):
        return self._board_scene(1,1,offset=-1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_equal(self):
        return self._board_scene(1,1,offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_above(self):
        return self._board_scene(1,1,offset=1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_below(self):
        return self._board_scene(3,3,offset=-1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_equal(self):
        return self._board_scene(3,3,offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_above(self):
        return self._board_scene(3,3,offset=1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_below(self):
        return self._board_scene(0,5,offset=-1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_equal(self):
        return self._board_scene(0,5,offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_above(self):
        return self._board_scene(0,5,offset=1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_below(self):
        return self._board_scene(5,0,offset=-1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_equal(self):
        return self._board_scene(5,0,offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_above(self):
        return self._board_scene(5,0,offset=1)

    @simulate(evidence={'text': ('destroy.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_protected_battlefields(self):
        return self._board_scene(3,3,protected=True)

