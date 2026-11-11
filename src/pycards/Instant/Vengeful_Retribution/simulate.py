from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Mountain.model import Mountain
from pycards.Instant.Vengeful_Retribution.model import Vengeful_Retribution


@bind_card(Vengeful_Retribution)
class Vengeful_Retribution_Simulation(Card_Simulation):
    text_parts = {
        "destroy.effect": [
            "Destroy {sacrifice_count} randomly chosen opposing creatures, or all if fewer exist.",
            "Randomly select up to {sacrifice_count} opposing creatures and destroy them, taking all if fewer.",
            "Destroy as many available opposing creatures as possible, up to {sacrifice_count}, choosing randomly.",
            "Choose {sacrifice_count} opposing creatures at random to destroy, or all available if fewer.",
            "Destroy up to {sacrifice_count} opposing creatures chosen randomly, taking all if fewer remain.",
            "Randomly pick opposing creatures without replacement and destroy up to {sacrifice_count} of them.",
            "Destroy a random set of up to {sacrifice_count} available opposing creatures.",
            "For {sacrifice_count} attempts, destroy a randomly chosen opposing creature not chosen earlier, if available.",
            "Choose and destroy opposing creatures randomly until {sacrifice_count} are chosen or none remain unchosen.",
            "Destroy {sacrifice_count} random opposing creatures if possible, or all available if fewer exist.",
        ],
        "damage.effect": [
            "If any unselected opposing creatures remain, deal damage equal to the selected creatures' total power to one random remaining creature.",
            "Deal the chosen creatures' combined pre-destruction power as damage to a random unselected opposing creature, if available.",
            "If an opposing creature was not selected for destruction, randomly pick one such creature to take damage equal to the selected creatures' total power.",
            "Add up the selected creatures' power and deal that damage to a random remaining unselected opposing creature, if any.",
            "A random opposing creature outside the selected set takes damage equal to that set's total power, if one remains.",
            "If available, hit one random unselected opposing creature for the combined power of the creatures selected for destruction.",
            "Use the selected creatures' total power as damage to a random opposing creature that was not selected, if possible.",
            "Randomly damage one of the unselected opposing creatures for the selected creatures' combined power, if one is available.",
            "Deal the sum of the selected creatures' power to a random other opposing creature, when any unselected one exists.",
            "If an unselected opposing creature is available, choose one randomly and deal damage equal to the selected creatures' combined power.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _effect_scene(self, own_count, enemy_count, protected=False, mountains=0, offset=0, role="enemy", hand_count=1, library_count=None, grave_count=0, tapped=False):
        self.scenario_prepare()
        self.player.hand.clear()
        self.player.graveyard.clear()
        self.player.opponent.graveyard.clear()
        for _ in range(hand_count):
            self.player.append_card(self.card.copy_for_player(self.player), "hand")
        for _ in range(mountains):
            land = Mountain(self.player)
            land.tap()
            self.stage_card(land, zone="land_area")
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                health = max(1, self.card.effect_params.get("damage", 3) + offset + index)
                creature = self.scenario_creature(owner, power=index + 1, health=health, flags={"tap": tapped, "Hexproof": False})
                if protected:
                    creature.gain_buff(Indestructible(self.card, creature), self.card)
        for owner in (self.player, self.player.opponent):
            for _ in range(grave_count):
                creature = self.scenario_creature(owner, power=2, health=3, flags={})
                owner.remove_card(creature, "battlefield")
                owner.append_card(creature, "graveyard")
        if library_count is not None:
            owner = self.player
            self.room.env_initinal_library(owner, {"instant_number": (library_count, library_count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)})
            owner.library = [card for card in owner.library if card.type == "Instant"][:library_count]
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('destroy.effect', 'damage.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0(self):
        return self._effect_scene(0, 0)

    @simulate(evidence={'text': ('destroy.effect', 'damage.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0(self):
        return self._effect_scene(1, 0)

    @simulate(evidence={'text': ('destroy.effect', 'damage.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1(self):
        return self._effect_scene(0, 1)

    @simulate(evidence={'text': ('destroy.effect', 'damage.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1(self):
        return self._effect_scene(1, 1)

    @simulate(evidence={'text': ('destroy.effect', 'damage.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3(self):
        return self._effect_scene(3, 3)

    @simulate(evidence={'text': ('destroy.effect', 'damage.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5(self):
        return self._effect_scene(0, 5)

    @simulate(evidence={'text': ('destroy.effect', 'damage.effect'), 'fields': ('mana_cost',)})
    def simulate_indestructible(self):
        return self._effect_scene(2, 5, mountains=3, protected=True)

