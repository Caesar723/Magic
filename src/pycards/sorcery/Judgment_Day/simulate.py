from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Mountain.model import Mountain
from pycards.sorcery.Judgment_Day.model import Judgment_Day


@bind_card(Judgment_Day)
class Judgment_Day_Simulation(Card_Simulation):
    text_parts = {
        "destroy.effect": [
            "Destroy all creatures on both battlefields.",
            "Destroy every creature controlled by either player.",
            "Destroy each creature on either battlefield.",
            "All creatures on both sides are destroyed.",
            "Mark all creatures in play for destruction.",
            "Destroy every creature currently in play.",
            "Apply destruction to all creatures on both sides.",
            "Destroy the creatures on both battlefields.",
            "Each creature in play is selected for destruction.",
            "Destroy every battlefield creature belonging to either player.",
        ],
        "return.effect": [
            "Then each player creates a fresh battlefield copy of a random creature in their graveyard, retaining the original there.",
            "After cleanup, each player copies one random creature from their graveyard onto their battlefield without removing the graveyard card.",
            "Each player then puts a fresh copy of a random graveyard creature onto their battlefield, leaving the original in the graveyard.",
            "Following destruction cleanup, create for each player a fresh battlefield copy of one random creature in their graveyard.",
            "Afterward, each player copies one of their graveyard creatures at random into play and leaves the original there.",
            "Then each player gets a fresh battlefield copy of a random creature from their graveyard, with the original still there.",
            "Each player copies a random creature from their own graveyard onto their battlefield after cleanup, retaining the original.",
            "After the destruction, each player puts a fresh copy of one random graveyard creature into play without moving the original.",
            "Next, each player creates one fresh battlefield copy from a random creature in their graveyard, leaving that card there.",
            "Following cleanup, return fresh battlefield copies of one random creature per player from their graveyards, preserving originals.",
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

    @simulate(evidence={'text': ('destroy.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0(self):
        return self._effect_scene(0, 0)

    @simulate(evidence={'text': ('destroy.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0(self):
        return self._effect_scene(1, 0)

    @simulate(evidence={'text': ('destroy.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1(self):
        return self._effect_scene(0, 1)

    @simulate(evidence={'text': ('destroy.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1(self):
        return self._effect_scene(1, 1)

    @simulate(evidence={'text': ('destroy.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3(self):
        return self._effect_scene(3, 3)

    @simulate(evidence={'text': ('destroy.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5(self):
        return self._effect_scene(0, 5)

    @simulate(evidence={'text': ('destroy.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_indestructible(self):
        return self._effect_scene(2, 5, mountains=3, protected=True)

    @simulate(evidence={'text': ('destroy.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_existing_graves_0(self):
        return self._effect_scene(2, 2, grave_count=0)

    @simulate(evidence={'text': ('destroy.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_existing_graves_1(self):
        return self._effect_scene(2, 2, grave_count=1)

    @simulate(evidence={'text': ('destroy.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_existing_graves_3(self):
        return self._effect_scene(2, 2, grave_count=3)

