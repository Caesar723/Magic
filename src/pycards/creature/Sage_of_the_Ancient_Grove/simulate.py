from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Sage_of_the_Ancient_Grove.model import Sage_of_the_Ancient_Grove


@bind_card(Sage_of_the_Ancient_Grove)
class Sage_of_the_Ancient_Grove_Simulation(Card_Simulation):
    text_parts = {
        "keyword.reach": [
            "Reach.",
            "This creature has reach.",
            "{card_name} has reach.",
            "This creature has the reach ability.",
            "{card_name} has the reach ability.",
            "This creature can block creatures with flying.",
            "{card_name} can block creatures with flying.",
            "Reach (This creature can block creatures with flying).",
            "This creature has reach and can block creatures with flying.",
            "{card_name} has reach and can block creatures with flying.",
        ],
        "enter.trigger": [
            "When {card_name} enters the battlefield,",
            "Whenever {card_name} enters the battlefield,",
            "When this creature enters the battlefield,",
            "Whenever this creature enters the battlefield,",
            "When {card_name} enters play,",
            "Whenever {card_name} enters play,",
            "When this creature enters play,",
            "Whenever this creature enters play,",
            "When {card_name} comes into play,",
            "Whenever {card_name} comes into play,",
        ],
        "enter.effect": [
            "Put the first basic land in your library onto your battlefield tapped, if one is available.",
            "If your library has a basic land, put its earliest one onto your battlefield tapped.",
            "Take the earliest basic land from your library and put it into play tapped, if possible.",
            "Move the first available basic land from your library onto your battlefield tapped.",
            "Your library's first basic land enters your battlefield tapped, if present.",
            "Find the first basic land in library order and put it into play tapped.",
            "Put the earliest available basic land in your library onto your battlefield in a tapped state.",
            "From your library, put the first basic land you find onto your battlefield tapped.",
            "If any basic lands remain in your library, move the first one into play tapped.",
            "Scan your library in order and put its first basic land onto your battlefield tapped.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    @simulate(evidence={'text': ('keyword.reach',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_block_flying_creature(self):
        return self.scenario_combat(True, False, False, enemy_flags={"flying": True})

    def _enter_library(self, basics, forests=0, nonbasic=False, only_lands=False):
        self.scenario_prepare()
        if only_lands:
            self.player.library.clear()
        else:
            self.player.library = [card for card in self.player.library if card.type != "Land"][:3]
        for _ in range(basics):
            self.player.library.append(Plains(self.player))
        for _ in range(forests):
            self.player.library.append(Forest(self.player))
        if nonbasic:
            land = Land(self.player)
            land.name, land.type = "Review nonbasic land", "Land"
            self.player.library.insert(0, land)
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_none(self):
        return self._enter_library(0, 0, nonbasic=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_plains_only(self):
        return self._enter_library(1, 0, nonbasic=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_forest_only(self):
        return self._enter_library(0, 1, nonbasic=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_many(self):
        return self._enter_library(3, 2, nonbasic=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_nonbasic_only(self):
        return self._enter_library(0, 0, nonbasic=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_mixed_nonbasic(self):
        return self._enter_library(1, 2, nonbasic=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_library(self):
        return self._enter_library(0, only_lands=True)

