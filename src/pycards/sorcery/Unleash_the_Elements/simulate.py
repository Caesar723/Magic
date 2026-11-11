from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.sorcery.Unleash_the_Elements.model import Unleash_the_Elements


@bind_card(Unleash_the_Elements)
class Unleash_the_Elements_Simulation(Card_Simulation):
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
        "exile.condition": [
            "If the creature is dead immediately after this damage, also mark it for exile.",
            "If a creature dies immediately from this damage, exile it.",
            "After the damage, exile each affected creature if it is a creature that is already dead.",
            "If the damaged creature is immediately dead, exile that creature.",
            "If each affected creature is a creature and is dead right after this damage, exile it.",
            "Exile each affected creature when it is a creature that dies immediately from this damage.",
            "If this damage immediately kills a creature, exile that creature.",
            "After dealing damage, exile each affected creatureed creature if it is now dead.",
            "If a creature is already dead immediately following this hit, exile it.",
            "Exile the creature if it is dead directly after taking this damage.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _board_scene(self, own_count, enemy_count, offset=0, protected=False, library_count=None, life=None, old_exile=False):
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
                    creature.gain_buff(Indestructible(self.card, creature), self.card)
            land = Plains(owner)
            land.tap()
            self.stage_card(land, owner, zone="land_area")
        if library_count is not None:
            self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "creature_number": (0, 0), "sorcery_number": (0, 0), "land_number": (0, 0)})
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_below(self):
        return self._board_scene(0, 0, offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_equal(self):
        return self._board_scene(0, 0, offset=0)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_above(self):
        return self._board_scene(0, 0, offset=1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_below(self):
        return self._board_scene(1, 0, offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_equal(self):
        return self._board_scene(1, 0, offset=0)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_above(self):
        return self._board_scene(1, 0, offset=1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_below(self):
        return self._board_scene(0, 1, offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_equal(self):
        return self._board_scene(0, 1, offset=0)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_above(self):
        return self._board_scene(0, 1, offset=1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_below(self):
        return self._board_scene(1, 1, offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_equal(self):
        return self._board_scene(1, 1, offset=0)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_above(self):
        return self._board_scene(1, 1, offset=1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_below(self):
        return self._board_scene(3, 3, offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_equal(self):
        return self._board_scene(3, 3, offset=0)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_above(self):
        return self._board_scene(3, 3, offset=1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_below(self):
        return self._board_scene(0, 5, offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_equal(self):
        return self._board_scene(0, 5, offset=0)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_above(self):
        return self._board_scene(0, 5, offset=1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_below(self):
        return self._board_scene(5, 0, offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_equal(self):
        return self._board_scene(5, 0, offset=0)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_above(self):
        return self._board_scene(5, 0, offset=1)

    @simulate(evidence={'text': ('damage.effect', 'exile.condition'), 'fields': ('mana_cost',)})
    def simulate_protected_battlefields(self):
        return self._board_scene(3, 3, protected=True)

