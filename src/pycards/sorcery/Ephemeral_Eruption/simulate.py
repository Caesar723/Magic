from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.sorcery.Ephemeral_Eruption.model import Ephemeral_Eruption


@bind_card(Ephemeral_Eruption)
class Ephemeral_Eruption_Simulation(Card_Simulation):
    scenario_locks={
        '_board_scene':('opponent.battlefield', 'opponent.land_area', 'self.battlefield', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "damage.effect": [
            "{card_name} deals {damage} damage to every creature.",
            "Deal {damage} damage to each creature on the battlefield.",
            "Every creature takes {damage} damage from {card_name}.",
            "Inflict {damage} damage on all creatures.",
            "Deal {damage} damage to all creatures on both sides.",
            "{card_name} hits each creature for {damage} damage.",
            "Each creature on either battlefield is dealt {damage} damage.",
            "{card_name} deals {damage} damage to all creatures in play.",
            "Deal an amount of damage equal to {damage} to each creature.",
            "All creatures take {damage} damage each.",
        ],
        "return.delayed": [
            "At your turn's end step, create fresh battlefield copies of the creatures that immediately died from this damage, leaving the originals in their graveyards.",
            "At the end of your turn, put fresh copies of this hit's immediately killed creatures onto their owners' battlefields without removing the graveyard originals.",
            "During your end step, bring back fresh copies of the creatures immediately killed by this hit while retaining the originals in their graveyards.",
            "When your turn ends, each creature immediately killed by this damage produces a fresh battlefield copy for its owner and remains in its graveyard.",
            "At your end step, copy the immediately killed creatures back to their owners' battlefields, preserving the graveyard cards.",
            "Your turn's end step returns fresh copies of this damage's immediate victims, with the originals still in their graveyards.",
            "At the end of your turn, restore fresh battlefield copies of the immediate victims without moving their graveyard originals.",
            "On your end step, each creature immediately killed by this damage is copied onto its owner's battlefield and stays in its graveyard.",
            "Fresh copies of the creatures immediately killed here appear on their owners' battlefields at your end step, while originals stay in their graveyards.",
            "When your end step occurs, create battlefield copies of this damage's immediate victims and retain their original graveyard cards.",
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
                creature.live = creature.actual_live = max(1, self.card.effect_params["damage"] + offset + index)
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

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_below(self):
        return self._board_scene(0,0,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_equal(self):
        return self._board_scene(0,0,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_above(self):
        return self._board_scene(0,0,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_below(self):
        return self._board_scene(1,0,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_equal(self):
        return self._board_scene(1,0,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_above(self):
        return self._board_scene(1,0,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_below(self):
        return self._board_scene(0,1,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_equal(self):
        return self._board_scene(0,1,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_above(self):
        return self._board_scene(0,1,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_below(self):
        return self._board_scene(1,1,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_equal(self):
        return self._board_scene(1,1,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_above(self):
        return self._board_scene(1,1,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_below(self):
        return self._board_scene(3,3,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_equal(self):
        return self._board_scene(3,3,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_above(self):
        return self._board_scene(3,3,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_below(self):
        return self._board_scene(0,5,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_equal(self):
        return self._board_scene(0,5,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_above(self):
        return self._board_scene(0,5,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_below(self):
        return self._board_scene(5,0,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_equal(self):
        return self._board_scene(5,0,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_above(self):
        return self._board_scene(5,0,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'return.delayed'), 'fields': ('mana_cost',)})
    def simulate_protected_battlefields(self):
        return self._board_scene(3,3,protected=True)

