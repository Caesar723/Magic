from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Call_of_the_Ancient_Ones.model import Call_of_the_Ancient_Ones


@bind_card(Call_of_the_Ancient_Ones)
class Call_of_the_Ancient_Ones_Simulation(Card_Simulation):
    text_parts = {
        "return.effect": [
            "Put a random creature card from either graveyard into your battlefield, if available.",
            "If there is a creature card from either graveyard, choose one randomly and put it into your battlefield.",
            "Choose a creature card from either graveyard at random and move it into your battlefield, if possible.",
            "Move one random creature card from either graveyard into your battlefield when available.",
            "Randomly select a creature card from either graveyard and put that card into your battlefield, if one exists.",
            "When any creature card from either graveyard is available, choose one at random to move into your battlefield.",
            "Put one available creature card from either graveyard, chosen randomly, into your battlefield.",
            "If possible, take a creature card from either graveyard chosen at random and put it into your battlefield.",
            "Move a randomly chosen creature card from either graveyard into your battlefield if any are available.",
            "Take a random creature card from either graveyard and move it into your battlefield, when one exists.",
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
                owner.append_card(creature, "graveyard")
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

