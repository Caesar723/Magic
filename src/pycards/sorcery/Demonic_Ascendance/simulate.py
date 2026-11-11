from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Demonic_Ascendance.model import Demonic_Ascendance


@bind_card(Demonic_Ascendance)
class Demonic_Ascendance_Simulation(Card_Simulation):
    text_parts = {
        "return.effect": [
            "Your opponent selects a creature from their hand to move onto your battlefield, if one is available.",
            "If your opponent has a creature in hand, they select one to enter your battlefield.",
            "Move an opposing hand creature selected by your opponent onto your battlefield, if possible.",
            "Your opponent chooses an available creature card from their hand and puts it onto your battlefield.",
            "Put a creature selected from your opponent's hand by that opponent onto your battlefield, if present.",
            "An available creature chosen by your opponent from their hand moves onto your battlefield.",
            "Let your opponent select a creature in their hand to put onto your battlefield, when available.",
            "Take one creature your opponent selects from their hand and put it onto your battlefield.",
            "If any creature is in the opposing hand, the opponent selects one to move onto your battlefield.",
            "Move one available creature card from your opponent's hand onto your battlefield, chosen by your opponent.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _recursion_scene(self, own_count, enemy_count=0, other_count=0, offset=0, colored=False, library_count=None, hand_count=0):
        self.scenario_prepare()
        self.player.graveyard.clear()
        self.player.opponent.graveyard.clear()
        self.player.hand.clear()
        self.player.opponent.hand.clear()
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                threshold = self.card.effect_params.get("mana_threshold", 2)
                cost = "W" * (threshold + offset + index + 1) if colored else str(max(0, threshold + offset + index))
                creature = self.scenario_creature(owner, power=index + 2, health=index + 3, flags={})
                creature.mana_cost = cost
                owner.remove_card(creature, "battlefield")
                owner.append_card(creature, "hand" if owner is self.player.opponent else "graveyard")
        for _ in range(other_count):
            self.player.append_card(self.card.copy_for_player(self.player), "graveyard")
        if library_count is not None:
            self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)})
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        for _ in range(hand_count):
            self.player.append_card(self.card.copy_for_player(self.player), "hand")
        return self.scenario_cast()

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_none(self):
        return self._recursion_scene(0, 0, 0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_one_own(self):
        return self._recursion_scene(1, 0, 0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_one_enemy(self):
        return self._recursion_scene(0, 1, 0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_both(self):
        return self._recursion_scene(1, 1, 0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_several(self):
        return self._recursion_scene(3, 3, 0)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_noncreatures(self):
        return self._recursion_scene(0, 0, 3)

    @simulate(evidence={'text': ('return.effect',), 'fields': ('mana_cost',)})
    def simulate_graves_mixed(self):
        return self._recursion_scene(3, 3, 3)

